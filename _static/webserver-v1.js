const source = new EventSource("/events");

source.addEventListener('log', function (e) {
    const log = document.getElementById("log");
    let log_prefs = [
        ["\u001b[1;31m", 'e'],
        ["\u001b[0;33m", 'w'],
        ["\u001b[0;32m", 'i'],
        ["\u001b[0;35m", 'c'],
        ["\u001b[0;36m", 'd'],
        ["\u001b[0;37m", 'v'],
        ];
    
    let klass = '';
    for (const log_pref of log_prefs){
        if (e.data.startsWith(log_pref[0])) {
            klass = log_pref[1];
        }
    }
    if (klass == ''){
        log.innerHTML += e.data + '\n';
    }
    log.innerHTML += '<span class="' + klass + '">' + e.data.substr(7, e.data.length - 11) + "</span>\n";
});

actions = [
    ["switch", ["toggle"]],
    ["light", ["toggle"]],
    ["cover", ["open", "close"]],
    ["button", ["press"]],
    ["lock", ["lock", "unlock", "open"]],
    ];

source.addEventListener('state', function (e) {
    const data = JSON.parse(e.data);
    document.getElementById(data.id).children[1].innerText = data.state;
});

const states = document.getElementById("states");
let i = 0, row;
for (; row = states.rows[i]; i++) {
    if (!row.children[2].children.length) {
        continue;
    }
    
    for (const domain of actions){
        if (row.classList.contains(domain[0])) {
            let id = row.id.substr(domain[0].length+1);
            domain[1].forEach( (action, j) => {
                row.children[2].children[j].addEventListener('click', function () {
                    const xhr = new XMLHttpRequest();
                    xhr.open("POST", '/'+domain[0]+'/' + id + '/' + action, true);
                    xhr.send();
                });
            });
        }
    }          
    if (row.classList.contains("select")) {
        (function(id) {
            row.children[2].children[0].addEventListener('change', function () {
                const xhr = new XMLHttpRequest();
                xhr.open("POST", '/select/' + id + '/set?option=' + encodeURIComponent(this.value), true);
                xhr.send();
            });
        })(row.id.substr(7));
    }
}
