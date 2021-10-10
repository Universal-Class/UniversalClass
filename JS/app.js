
// USING DUMMY JSON DATA FOR TESTING
const data = [
    {
        "end_time": "12-12-12 1:5:3",
        "id": "RJSHNJKKUqeyvj7UWEMuH1x7qms3",
        "link": "meets.google.com/xxx",
        "start_time": "12-12-12 1:5:2",
        "teacher_name": "Dr. Jake Peralta",
        "university": "Amrita University",
        "name_of_class": "K Nearest Neighbour",
        "label": "Machine Learning"
    },
    {
        "end_time": "12-12-12 1:7:3",
        "id": "RJSHNJKKUqeyvj7UWEMuH1x7qms3",
        "link": "meets.google.com/yyy",
        "start_time": "12-12-12 1:6:2",
        "teacher_name": "Dr. Raymond Holt",
        "university": "Stanford University",
        "name_of_class": "K Nearest Neighbour",
        "label": "Machines"
    },
    {
        "end_time": "12-12-12 1:7:3",
        "id": "RJSHNJKKUqeyvj7UWEMuH1x7qms3",
        "link": "meets.google.com/yyy",
        "start_time": "12-12-12 1:6:2",
        "teacher_name": "Dr. Amy Santiago",
        "university": "IIT Warangal",
        "name_of_class": "K Nearest Neighbour",
        "label": "Computer Science"
    },
]

function myFunction(data) {

    document.getElementById("class-list").innerHTML = `
        ${data.map(function (classInfo) {
        return `
                <li>
                <div class="info">
            
                    <span class="name">${classInfo.name_of_class}</span>
                    <span class="about">${classInfo.teacher_name}</span>
                    <span class="about">${classInfo.start_time} to ${classInfo.end_time}</span>
                    <span class="about">${classInfo.university}</span>
                    <span class="about" id="label">${classInfo.label}</span>
                </div>
                <a href="${classInfo.link}">
                <span class="link">Join live class</span>
                </a>
                </li>
            `
    }).join('')}
    `
}

myFunction(data);
makeRequest()

var g = document.getElementById("preferences").checked;
console.log(g)
var checkbox = document.querySelector("input[name=preferences]");
checkbox.addEventListener('change', function () {
    var g = this.checked;
    if (g) {
        console.log(g);
        console.log("Checkbox is checked..");
        makeRequest()
    } else {
        console.log(g);
        console.log("Checkbox is not checked..");
        makeRequest()
    }
});

function makeRequest() {
    var xmlhttp = new XMLHttpRequest();
    var url = "http://universalclass.pythonanywhere.com/get_data";
    id = firebase.auth().currentUser.uid
    console.log(id)
    xmlhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            myFunction(data);
        }
    };
    xmlhttp.open("POST", url, true);
    xmlhttp.send();
}



const list = document.querySelector('#class-list')
const searchBar = document.forms['search-class'].querySelector('input');
searchBar.addEventListener('keyup', function (e) {
    const term = e.target.value.toLowerCase();
    const labels = list.getElementsByTagName('li');
    Array.from(labels).forEach(function (label) {
        const title = label.firstElementChild.children[4].textContent;
        console.log(title)
        if (title.toLowerCase().indexOf(term) != -1) {
            label.style.display = "";
        }
        else {
            label.style.display = "none";
        }
    })
})