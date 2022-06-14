// CONSTANTS -------------------------------------------------------------------

const mainHeader = document.querySelector("#mainHeader");
const mainDataDiv = document.querySelector("#mainDataDiv");
const detailsDataDiv = document.querySelector("#detailsDataDiv");


// CLASSES ---------------------------------------------------------------------

class Machine {

    static mainDatafieldsParams = [
        {
            title: "Empresa",
            field: "company",
            parser: (fieldValue) => fieldValue
        },
        {
            title: "Clase",
            field: "class",
            parser: (fieldValue) => fieldValue
        },
        {
            title: "Estado",
            field: "working",
            parser: (fieldValue) => fieldValue ? "Trabajando" : "Sin actividad"
        },
        {
            title: "Última actualización",
            field: "lastUpdate",
            parser: (fieldValue) => new Date(fieldValue).toLocaleString('es-AR')
        },
    ];

    constructor(id) {
        this.id;
        this.description;
        this.working;
        this.moving;
        this.chasis;
        this.class;
        this.company;
        this.lastUpdate;
        this.data;
    }

    async updateAllFields(id) {
        this.id = id;
        let obj;
        try {
            const response = await axios({
                method: "get",
                baseURL: mainAPIURL,
                url: "machines/" + this.id
            });
            obj = response.data;
        }
        catch (error) {
            obj = {};
        }
        this.description = obj.description;
        this.working = obj.working;
        this.moving = obj.moving;
        this.chasis = obj.chasis;
        this.class = obj.class;
        this.company = obj.company;
        this.lastUpdate = obj.last_update; // this is different!
        this.data = obj.data;
    }

    makeMainHeader() {
        const descriptionSpan = document.createElement("span");
        const idSpan = document.createElement("span");

        descriptionSpan.textContent = this.description;
        idSpan.textContent = String(this.id);
        idSpan.id = "mainHeaderidSpan";

        mainHeader.appendChild(descriptionSpan);
        mainHeader.appendChild(idSpan);
    }

    makeMainData() {
        for (const fieldObj of Machine.mainDatafieldsParams) {
            const div = document.createElement("div");
            const h2 = document.createElement("h2");
            h2.textContent = fieldObj.title;
            const p = document.createElement("p");
            p.textContent = fieldObj.parser(this[fieldObj.field]);

            div.appendChild(h2);
            div.appendChild(p);

            mainDataDiv.appendChild(div);
        }
    }

    makeDetailsData() {
        for (const key in this.data) {
            const category = this.data[key];
            const table = document.createElement("table");
            const thead = table.createTHead();
            const tbody = table.createTBody();
            const th = document.createElement("th");

            th.setAttribute("colspan", 2);
            th.textContent = key;
            thead.appendChild(th);

            for (const key in category) {
                if (Object.hasOwnProperty.call(category, key)) {
                    const value = category[key];
                    const row = tbody.insertRow();

                    const measureCell = row.insertCell();
                    measureCell.textContent = key;
                    measureCell.classList.add("measureCell");

                    const valueCell = row.insertCell();
                    valueCell.textContent = value;
                    valueCell.classList.add("valueCell");
                }
            }

            detailsDataDiv.appendChild(table);
        }
    }
}


// FUNCTIONS -------------------------------------------------------------------

async function make() {
    const machine = new Machine();
    await machine.updateAllFields(requestParams.id);
    await machine.makeMainHeader();
    await machine.makeMainData();
    await machine.makeDetailsData();
}


// EVENT LISTENERS -------------------------------------------------------------

searchForm.addEventListener("submit", async (evt) => {
    evt.preventDefault();
})

searchInput.addEventListener("change", async (evt) => {
    newURL = mainURL + "?search=" + searchInput.value;
    console.log(newURL);
    window.location.href = newURL;
})


// EXECUTE ON START ------------------------------------------------------------

make();