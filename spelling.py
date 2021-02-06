
try:
from enchant.tokenize import Filter, get_tokenizer, tokenize, unit_tokenize
from xmlrpc import client as xmlrpc_client
import subprocess
import imp
import builtins
from . import checker, filters
from sphinx.util.osutil import ensuredir
from sphinx.util.matching import Matcher
from sphinx.util.console import red
from sphinx.builders import Builder
import docutils.nodes
from docutils.parsers import rst
import tempfile
import os
import importlib
from sphinx.environment.collectors import EnvironmentCollector
import contextlib
import collections
# For Python 3.8 and later
import importlib.metadata as importlib_metadata
except ImportError:
    # For everyone else
    import importlib_metadata

from sphinx.util import logging

from .asset import SpellingCollector
from .builder import SpellingBuilder
from .directive import SpellingDirective

logger = logging.getLogger(__name__)

#
# Copyright (c) 2020 Doug Hellmann.  All rights reserved.
#
"""Asset collector for additional spelling terms."""


try:
    from enchant.tokenize import EmailFilter, WikiWordFilter
except ImportError as imp_exc:
    enchant_import_error = imp_exc
else:
    enchant_import_error = None

try:
    import enchant
    from enchant.tokenize import get_tokenizer
except ImportError as imp_exc:
    enchant_import_error = imp_exc
else:
    enchant_import_error = None


logger = logging.getLogger(__name__)


# TODO - Words with multiple uppercase letters treated as classes and ignored


class AcronymFilter(Filter):
    """If a word looks like an acronym (all upper case letters),
    ignore it.
    """

    def _skip(self, word):
        return (
            word.isupper() or  # all caps
            # pluralized acronym ("URLs")
            (word[-1].lower() == 's' and word[:-1].isupper())
        )


class list_tokenize(tokenize):

    def __init__(self, words):
        super().__init__('')
        self._words = words

    def next(self):
        if not self._words:
            raise StopIteration()
        word = self._words.pop(0)
        return (word, 0)


class ContractionFilter(Filter):
    """Strip common contractions from words.
    """
    splits = {
        "aren't": ["are", "not"],
        "can't": ["can", "not"],
        "could've": ["could", "have"],
        "couldn't": ["could", "not"],
        "didn't": ["did", "not"],
        "doesn't": ["does", "not"],
        "don't": ["do", "not"],
        "hadn't": ["had", "not"],
        "hasn't": ["has", "not"],
        "haven't": ["have", "not"],
        "he'd": ["he", "would"],
        "he'll": ["he", "will"],
        "he's": ["he", "is"],
        "how'd": ["how", "would"],
        "how'll": ["how", "will"],
        "how's": ["how", "is"],
        "i'd": ["I", "would"],
        "i'll": ["I", "will"],
        "i'm": ["I", "am"],
        "i've": ["I", "have"],
        "isn't": ["is", "not"],
        "it'd": ["it", "would"],
        "it'll": ["it", "will"],
        "it's": ["it", "is"],
        "ma'am": ["madam"],
        "might've": ["might", "have"],
        "mightn't": ["might", "not"],
        "must've": ["must", "have"],
        "mustn't": ["must", "not"],
        "o'": ["of"],
        "o'clock": ["of", "the", "clock"],
        "she'd": ["she", "would"],
        "she'll": ["she", "will"],
        "she's": ["she", "is"],
        "should've": ["should", "have"],
        "shouldn't": ["should", "not"],
        "that'd": ["that", "would"],
        "that'll": ["that", "will"],
        "that's": ["that", "is"],
        "they'd": ["they", "would"],
        "they'll": ["they", "will"],
        "they're": ["they", "are"],
        "they've": ["they", "have"],
        "wasn't": ["was", "not"],
        "we'd": ["we", "would"],
        "we'll": ["we", "will"],
        "we're": ["we", "are"],
        "we've": ["we", "have"],
        "weren't": ["were", "not"],
        "what'd": ["what", "would"],
        "what'll": ["what", "will"],
        "what're": ["what", "are"],
        "what's": ["what", "is"],
        "when'd": ["when", "would"],
        "when'll": ["when", "will"],
        "when's": ["when", "is"],
        "where'd": ["where", "would"],
        "where'll": ["where", "will"],
        "where's": ["where", "is"],
        "who'd": ["who", "would"],
        "who'll": ["who", "will"],
        "who's": ["who", "is"],
        "why'd": ["why", "would"],
        "why'll": ["why", "will"],
        "why's": ["why", "is"],
        "won't": ["will", "not"],
        "would've": ["would", "have"],
        "wouldn't": ["would", "not"],
        "you'd": ["you", "would"],
        "you'll": ["you", "will"],
        "you're": ["you", "are"],
        "you've": ["you", "have"],
    }

    def _split(self, word):
        # Fixed responses
        if word.lower() in self.splits:
            return list_tokenize(self.splits[word.lower()])

        # Possessive
        if word.lower().endswith("'s"):
            return unit_tokenize(word[:-2])

        # * not
        if word.lower().endswith("n't"):
            return unit_tokenize(word[:-3])

        return unit_tokenize(word)


class IgnoreWordsFilter(Filter):
    """Given a set of words, ignore them all.
    """

    def __init__(self, tokenizer, word_set):
        self.word_set = set(word_set)
        super().__init__(tokenizer)

    def _skip(self, word):
        return word in self.word_set


class IgnoreWordsFilterFactory:

    def __init__(self, words):
        self.words = words

    def __call__(self, tokenizer):
        return IgnoreWordsFilter(tokenizer, self.words)


class PyPIFilterFactory(IgnoreWordsFilterFactory):
    """Build an IgnoreWordsFilter for all of the names of packages on PyPI.
    """

    def __init__(self):
        client = xmlrpc_client.ServerProxy('https://pypi.python.org/pypi')
        super().__init__(client.list_packages())


class PythonBuiltinsFilter(Filter):
    """Ignore names of built-in Python symbols.
    """

    def _skip(self, word):
        return hasattr(builtins, word)


class ImportableModuleFilter(Filter):
    """Ignore names of modules that we could import.
    """

    def __init__(self, tokenizer):
        super().__init__(tokenizer)
        self.found_modules = set()
        self.sought_modules = set()

    def _skip(self, word):
        if word not in self.sought_modules:
            self.sought_modules.add(word)
            try:
                imp.find_module(word)
            except ImportError:
                return False
            self.found_modules.add(word)
            return True
        return word in self.found_modules


class ContributorFilter(IgnoreWordsFilter):
    """Accept information about contributors as spelled correctly.
    Look in the git history for authors and committers and accept
    tokens that are in the set.
    """

    _pretty_format = (
        '%(trailers:key=Co-Authored-By,separator=%x0A)%x0A%an%x0A%cn'
    )

    def __init__(self, tokenizer):
        contributors = self._get_contributors()
        super().__init__(tokenizer, contributors)

    def _get_contributors(self):
        logger.info('Scanning contributors')
        cmd = [
            'git', 'log', '--quiet', '--no-color',
            '--pretty=format:' + self._pretty_format,
        ]
        try:
            p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as err:
            logger.warning('Called: {}'.format(' '.join(cmd)))
            logger.warning(f'Failed to scan contributors: {err}')
            return set()
        output = p.stdout.decode('utf-8')
        tokenizer = get_tokenizer('en_US', filters=[])
        return {word for word, pos in tokenizer(output)}


class SpellingDirective(rst.Directive):
    """Custom directive for passing instructions to the spelling checker.
    .. spelling::
       word1
       word2
    """

    has_content = True

    def run(self):
        env = self.state.document.settings.env

        # Initialize the per-document good words list
        if not hasattr(env, 'spelling_document_words'):
            env.spelling_document_words = collections.defaultdict(list)

        good_words = []
        for entry in self.content:
            if not entry:
                continue
            good_words.extend(entry.split())
        if good_words:
            logger.debug(
                'Extending local dictionary for %s with %s' % (
                    env.docname, str(good_words))
            )
            env.spelling_document_words[env.docname].extend(good_words)

        return []


class SpellingBuilder(Builder):
    """
    Spell checks a document
    """
    name = 'spelling'

    def init(self):
        if enchant_import_error is not None:
            raise RuntimeError(
                'Cannot initialize spelling builder '
                'without PyEnchant installed') from enchant_import_error
        self.misspelling_count = 0

        self.env.settings["smart_quotes"] = False
        # Initialize the per-document filters
        if not hasattr(self.env, 'spelling_document_words'):
            self.env.spelling_document_words = collections.defaultdict(list)

        # Initialize the global filters
        f = [
            filters.ContractionFilter,
            EmailFilter,
        ]
        if self.config.spelling_ignore_wiki_words:
            logger.info('Ignoring wiki words')
            f.append(WikiWordFilter)
        if self.config.spelling_ignore_acronyms:
            logger.info('Ignoring acronyms')
            f.append(filters.AcronymFilter)
        if self.config.spelling_ignore_pypi_package_names:
            logger.info('Adding package names from PyPI to local dictionary…')
            f.append(filters.PyPIFilterFactory())
        if self.config.spelling_ignore_python_builtins:
            logger.info('Ignoring Python builtins')
            f.append(filters.PythonBuiltinsFilter)
        if self.config.spelling_ignore_importable_modules:
            logger.info('Ignoring importable module names')
            f.append(filters.ImportableModuleFilter)
        if self.config.spelling_ignore_contributor_names:
            logger.info('Ignoring contributor names')
            f.append(filters.ContributorFilter)
        f.extend(self._load_filter_classes(self.config.spelling_filters))

        if not os.path.isdir(self.outdir):
            os.mkdir(self.outdir)

        word_list = self.get_wordlist_filename()
        logger.info(f'Looking for custom word list in {word_list}')

        self.checker = checker.SpellingChecker(
            lang=self.config.spelling_lang,
            tokenizer_lang=self.config.tokenizer_lang,
            suggest=self.config.spelling_show_suggestions,
            word_list_filename=word_list,
            filters=f,
            context_line=self.config.spelling_show_whole_line,
        )

    def _load_filter_classes(self, filters):
        # Filters may be expressed in the configuration file using
        # names, so look through them and import the referenced class
        # and use that in the checker.
        for filter in filters:
            if not isinstance(filter, str):
                yield filter
                continue
            module_name, _, class_name = filter.rpartition('.')
            mod = importlib.import_module(module_name)
            yield getattr(mod, class_name)

    def get_wordlist_filename(self):
        word_list = self.config.spelling_word_list_filename
        if word_list is None:
            word_list = 'spelling_wordlist.txt'

        if not isinstance(word_list, list):
            filename = os.path.join(self.srcdir, word_list)
            return filename

        # In case the user has multiple word lists, we combine them
        # into one large list that we pass on to the checker.
        return self._build_combined_wordlist()

    def _build_combined_wordlist(self):
        # If we have a list, the combined list is the first list plus all words
        # from the other lists. Otherwise, word_list is assumed to just be a
        # string.
        temp_dir = tempfile.mkdtemp()
        combined_word_list = os.path.join(temp_dir,
                                          'spelling_wordlist.txt')

        word_list = self.config.spelling_word_list_filename

        with open(combined_word_list, 'w', encoding='UTF-8') as outfile:
            for word_file in word_list:
                # Paths are relative
                long_word_file = os.path.join(self.srcdir, word_file)
                logger.info('Adding contents of {} to custom word list'.format(
                    long_word_file))
                with open(long_word_file, encoding='UTF-8') as infile:
                    infile_contents = infile.readlines()
                outfile.writelines(infile_contents)

                # Check for newline, and add one if not present
                if infile and not infile_contents[-1].endswith('\n'):
                    outfile.write('\n')

        return combined_word_list

    def get_outdated_docs(self):
        return 'all documents'

    def prepare_writing(self, docnames):
        return

    def get_target_uri(self, docname, typ=None):
        return ''

    def format_suggestions(self, suggestions):
        if not self.config.spelling_show_suggestions or not suggestions:
            return ''
        return '[' + ', '.join('"%s"' % s for s in suggestions) + ']'

    TEXT_NODES = {
        'block_quote',
        'paragraph',
        'list_item',
        'term',
        'definition_list_item',
        'title',
    }

    def write_doc(self, docname, doctree):
        lines = list(self._find_misspellings(docname, doctree))
        self.misspelling_count += len(lines)
        if lines:
            output_filename = os.path.join(self.outdir, docname + '.spelling')
            logger.info('Writing %s', output_filename)
            ensuredir(os.path.dirname(output_filename))
            with open(output_filename, 'w', encoding='UTF-8') as output:
                output.writelines(lines)

    def _find_misspellings(self, docname, doctree):

        excluded = Matcher(self.config.spelling_exclude_patterns)
        if excluded(self.env.doc2path(docname, None)):
            return
        # Build the document-specific word filter based on any good
        # words listed in spelling directives. If we have no such
        # words, we want to push an empty list of filters so that we
        # can always safely pop the filter stack when we are done with
        # this document.
        doc_filters = []
        good_words = self.env.spelling_document_words.get(docname)
        if good_words:
            logger.info('Extending local dictionary for %s', docname)
            doc_filters.append(filters.IgnoreWordsFilterFactory(good_words))
        self.checker.push_filters(doc_filters)

        for node in doctree.traverse(docutils.nodes.Text):
            if (node.tagname == '#text' and
                    node.parent and
                    node.parent.tagname in self.TEXT_NODES):

                # Figure out the line number for this node by climbing the
                # tree until we find a node that has a line number.
                lineno = None
                parent = node
                seen = set()
                while lineno is None:
                    # logger.info('looking for line number on %r' % node)
                    seen.add(parent)
                    parent = node.parent
                    if parent is None or parent in seen:
                        break
                    lineno = parent.line

                # Check the text of the node.
                misspellings = self.checker.check(node.astext())
                for word, suggestions, context_line in misspellings:
                    msg_parts = ['Spell check', red(word)]
                    if self.format_suggestions(suggestions) != '':
                        msg_parts.append(self.format_suggestions(suggestions))
                    msg_parts.append(context_line)
                    msg = ': '.join(msg_parts) + '.'
                    loc = (docname, lineno) if lineno else docname
                    if self.config.spelling_warning:
                        logger.warning(msg, location=loc)
                    else:
                        logger.info(msg, location=loc)
                    yield "%s:%s: (%s) %s %s\n" % (
                        self.env.doc2path(docname, None),
                        lineno, word,
                        self.format_suggestions(suggestions),
                        context_line,
                    )

        self.checker.pop_filters()
        return

    def finish(self):
        if self.misspelling_count:
            logger.warning('Found %d misspelled words' %
                           self.misspelling_count)
        return


class SpellingChecker:
    """Checks the spelling of blocks of text.
    Uses options defined in the sphinx configuration file to control
    the checking and filtering behavior.
    """

    def __init__(self, lang, suggest, word_list_filename,
                 tokenizer_lang='en_US', filters=None, context_line=False):
        if enchant_import_error is not None:
            raise RuntimeError(
                'Cannot instantiate SpellingChecker '
                'without PyEnchant installed',
            ) from enchant_import_error
        if filters is None:
            filters = []
        self.dictionary = enchant.DictWithPWL(lang, word_list_filename)
        self.tokenizer = get_tokenizer(tokenizer_lang, filters=filters)
        self.original_tokenizer = self.tokenizer
        self.suggest = suggest
        self.context_line = context_line

    def push_filters(self, new_filters):
        """Add a filter to the tokenizer chain.
        """
        t = self.tokenizer
        for f in new_filters:
            t = f(t)
        self.tokenizer = t

    def pop_filters(self):
        """Remove the filters pushed during the last call to push_filters().
        """
        self.tokenizer = self.original_tokenizer

    def check(self, text):
        """Yields bad words and suggested alternate spellings.
        """
        for word, pos in self.tokenizer(text):
            correct = self.dictionary.check(word)
            if correct:
                continue

            suggestions = self.dictionary.suggest(word) if self.suggest else []
            line = line_of_index(text, pos) if self.context_line else ""

            yield word, suggestions, line
        return


def line_of_index(text, index):
    try:
        line_start = text.rindex("\n", 0, index) + 1
    except ValueError:
        line_start = 0
    try:
        line_end = text.index("\n", index)
    except ValueError:
        line_end = len(text)

    return text[line_start:line_end]


class SpellingCollector(EnvironmentCollector):

    def clear_doc(self, app, env, docname) -> None:
        with contextlib.suppress(AttributeError, KeyError):
            del env.spelling_document_words[docname]

    def merge_other(self, app, env, docnames, other):
        try:
            other_words = other.spelling_document_words
        except AttributeError:
            other_words = {}

        if not hasattr(env, 'spelling_document_words'):
            env.spelling_document_words = collections.defaultdict(list)
        env.spelling_document_words.update(other_words)

    def process_doc(self, app, doctree):
        pass


def setup(app):
    version = importlib_metadata.version('sphinxcontrib-spelling')
    logger.info('Initializing Spelling Checker %s', version)
    app.add_builder(SpellingBuilder)
    # Register the 'spelling' directive for setting parameters within
    # a document
    app.add_directive('spelling', SpellingDirective)
    # Register an environment collector to merge data gathered by the
    # directive in parallel builds
    app.add_env_collector(SpellingCollector)
    # Report guesses about correct spelling
    app.add_config_value('spelling_show_suggestions', False, 'env')
    # Report the whole line that has the error
    app.add_config_value('spelling_show_whole_line', True, 'env')
    # Emit misspelling as a sphinx warning instead of info message
    app.add_config_value('spelling_warning', False, 'env')
    # Set the language for the text
    app.add_config_value('spelling_lang', 'en_US', 'env')
    # Set the language for the tokenizer
    app.add_config_value('tokenizer_lang', 'en_US', 'env')
    # Set a user-provided list of words known to be spelled properly
    app.add_config_value('spelling_word_list_filename',
                         None,
                         'env')
    # Assume anything that looks like a PyPI package name is spelled properly
    app.add_config_value('spelling_ignore_pypi_package_names', False, 'env')
    # Assume words that look like wiki page names are spelled properly
    app.add_config_value('spelling_ignore_wiki_words', True, 'env')
    # Assume words that are all caps, or all caps with trailing s, are
    # spelled properly
    app.add_config_value('spelling_ignore_acronyms', True, 'env')
    # Assume words that are part of __builtins__ are spelled properly
    app.add_config_value('spelling_ignore_python_builtins', True, 'env')
    # Assume words that look like the names of importable modules are
    # spelled properly
    app.add_config_value('spelling_ignore_importable_modules', True, 'env')
    # Treat contributor names from git history as spelled correctly
    app.add_config_value('spelling_ignore_contributor_names', True, 'env')
    # Add any user-defined filter classes
    app.add_config_value('spelling_filters', [], 'env')
    # Set a user-provided list of files to ignore
    app.add_config_value('spelling_exclude_patterns',
                         [],
                         'env')
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
        "version": version,
    }
