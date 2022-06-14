// CONSTANTS -------------------------------------------------------------------

const searchInput = document.querySelector("#searchInput");
const searchForm = document.querySelector("#searchForm");
const machinesList = document.querySelector("#machinesList");


// CLASSES ---------------------------------------------------------------------

class Machine {
    constructor(obj) {
        this.id = obj.id;
        this.description = obj.description;
        this.working = obj.working;
    }

    toString() {
        return String(this.id) + " - " + this.description + " - " + this.working;
    }

    makeListItem() {
        const textDiv = document.createElement("div");
        const idSpan = document.createElement("span");
        const descriptionSpan = document.createElement("span");
        const workingSpan = document.createElement("span");

        textDiv.classList.add("textDiv");
        idSpan.classList.add("idSpan");
        idSpan.textContent = "(" + this.id + ") ";
        descriptionSpan.textContent = this.description;

        workingSpan.classList.add("circle");
        if (this.working) {
            workingSpan.classList.add("workingTrue");
        }
        else {
            workingSpan.classList.add("workingFalse");
        }

        const li = document.createElement("li");
        li.setAttribute("id", this.id);
        textDiv.appendChild(idSpan);
        textDiv.appendChild(descriptionSpan);
        li.appendChild(textDiv);
        li.appendChild(workingSpan);

        return li;
    }
}


// FUNCTIONS -------------------------------------------------------------------

async function fetchMachines(queryText) {
    let machinesObj;
    try {
        const response = await axios({
            method: "get",
            baseURL: mainAPIURL,
            url: "machines",
            params: {
                q: queryText
            }
        });
        if (Array.isArray(response.data)) {
            machinesObj = response.data;
        }
        else {
            machinesObj = [response.data];
        }
    }
    catch (error) {
        machinesObj = [];
    }

    if (queryText == "" && machinesObj.length != 0) {
        machinesObj = machinesObj.slice(0, 5);
    }
    return machinesObj;
}

async function getMachines(queryText) {
    const machines = [];
    const machinesObj = await fetchMachines(queryText);
    if (machinesObj) {
        for (const obj of machinesObj) {
            const machine = new Machine(obj);
            machines.push(machine);
        }
    }
    return machines;
}

async function updateList(machines) {
    removeChilds(machinesList);
    for (const machine of machines) {
        machinesList.appendChild(machine.makeListItem());
    }
}

function removeChilds(parent) {
    while (parent.lastChild) {
        parent.removeChild(parent.lastChild);
    }
};


// EVENT LISTENERS -------------------------------------------------------------

searchInput.addEventListener("input", async (evt) => {
    queryText = searchInput.value;
    const machines = await getMachines(queryText);
    await updateList(machines);
})

searchForm.addEventListener("submit", async (evt) => {
    evt.preventDefault();
})

machinesList.addEventListener("click", async (evt) => {
    let currentNode = evt.target;
    while (currentNode.nodeName != "LI") {
        currentNode = currentNode.parentNode;
    }

    machineURL = mainURL + currentNode.getAttribute("id");

    window.location.href = machineURL;

});


// EXECUTE ON START ------------------------------------------------------------

// add the optional param
searchInput.value = requestParams.search;

// trigger the first request
const evt = new Event("input");
searchInput.dispatchEvent(evt);