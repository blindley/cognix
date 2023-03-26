
function findAncestorWithClass(node, className) {
    let current = node;

    while (current !== null) {
        if (current.classList && current.classList.contains(className)) {
            return current;
        }
        current = current.parentNode;
    }

    return null;
}

function initCardEditor() {
    initFixedFields();

    const cardDataElement = document.getElementById("card-data");
    if (cardDataElement) {
        const cardData = JSON.parse(cardDataElement.textContent);
        for (const key in cardData) {
            if (!["cognix.cardTemplate", "cognix.instanceCount"].includes(key)) {
                addRow(false, key, cardData[key], false);
            }
        }
    }
}

function initFixedFields() {
    addRow(false, 'cognix.cardTemplate', 'cognix.basic', true);
    addRow(false, 'cognix.instanceCount', 1, true);
    document.getElementById("new-field-button").focus();
}

function deleteRow(node) {
    row = findAncestorWithClass(node, "field-row");
    row.parentNode.removeChild(row);
}

function addRow(focus = false, keyName = null, value = null, fixedKey = false) {
    const table = document.getElementById("card-data-table");
    const rowIndex = table.rows.length;

    const row = table.insertRow(-1);
    row.classList.add('field-row');

    const keyCell = row.insertCell(0);
    const valueCell = row.insertCell(1);
    const deleteButtonCell = row.insertCell(2);

    const keyInput = document.createElement('input');
    keyInput.type = 'text';
    keyInput.className = 'key';
    keyInput.disabled = fixedKey;

    const valueInput = document.createElement('input');
    valueInput.type = 'text';
    valueInput.className = 'value';
    valueInput.onkeydown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addRow(true);
        }
    };

    const keyCheckbox = document.createElement('input');
    keyCheckbox.type = 'checkbox';
    keyCheckbox.className = 'sticky-key-checkbox';
    keyCheckbox.disabled = fixedKey;
    keyCheckbox.checked = fixedKey;
    keyCheckbox.title = 'Make key sticky'; // Add hover text
    keyCheckbox.onchange = () => {
        if (!keyCheckbox.checked) {
            valueCheckbox.checked = false;
        }
    };

    const valueCheckbox = document.createElement('input');
    valueCheckbox.type = 'checkbox';
    valueCheckbox.className = 'sticky-value-checkbox';
    valueCheckbox.checked = fixedKey;
    valueCheckbox.title = 'Make value sticky'; // Add hover text
    valueCheckbox.onchange = () => {
        if (valueCheckbox.checked) {
            keyCheckbox.checked = true;
        }
    };

    keyCell.prepend(keyCheckbox);
    valueCell.prepend(valueCheckbox);

    if (!fixedKey) {
        deleteButtonCell.innerHTML = '<button onclick="deleteRow(this)">Delete</button>';
    }

    keyInput.value = keyName || '';
    valueInput.value = value || '';

    keyCell.appendChild(keyInput);
    valueCell.appendChild(valueInput);

    if (focus) {
        if (fixedKey) {
            valueCheckbox.focus()
        } else {
            keyCheckbox.focus();
        }
    }
}

function resetFields() {
    const table = document.getElementById("card-data-table");

    for (let i = table.rows.length - 1; i >= 2; i--) { // Start from the index 2 to skip the fixed fields
        const row = table.rows[i];
        const keyInput = row.cells[0].getElementsByTagName("input")[1]; // Get the key input
        const valueInput = row.cells[1].getElementsByTagName("input")[1]; // Get the value input
        const keyCheckbox = row.cells[0].getElementsByTagName("input")[0]; // Get the key checkbox
        const valueCheckbox = row.cells[1].getElementsByTagName("input")[0]; // Get the value checkbox

        if (!keyCheckbox.checked) {
            table.deleteRow(i);
        } else {
            if (!valueCheckbox.checked) {
                valueInput.value = "";
            }
        }
    }
}

async function submitForm() {
    const cardData = {};
    const keys = document.getElementsByClassName("key");
    const values = document.getElementsByClassName("value");

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i].value;
        const value = values[i].value;

        cardData[key] = value;
    }

    const requestData = {
        uuid: document.getElementById("card-uuid") ? document.getElementById("card-uuid").textContent : null,
        cardData: cardData
    };

    const response = await fetch('/submit-card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    });

    if (response.ok) {
        const result = await response.json();
        if (result.success) {
            document.getElementById("result").innerText = "Card data processed successfully!";
            resetFields();

            // Clear the UUID and update the address bar
            if (document.getElementById("card-uuid")) {
                document.getElementById("card-uuid").textContent = "";
            }
            window.history.pushState({}, "", "/card-editor");

        } else {
            const errors = result.errors.join("\n");
            document.getElementById("result").innerText = `Error processing Card data:\n${errors}`;
        }
    } else {
        document.getElementById("result").innerText = "Error sending Card data.";
    }
}


async function searchCards() {
    const keys = document.getElementsByClassName("key");
    const values = document.getElementsByClassName("value");
    let searchDict = {};

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i].value;
        const value = values[i].value;
        
        if (key && value) {
            searchDict[key] = value;
        }
    }

    const response = await fetch('/search-cards', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(searchDict)
    });

    const result = await response.json();
    displaySearchResults(result);
}


function displaySearchResults(results) {
    const tableBody = document.getElementById("search-results-table-body");
    tableBody.innerHTML = "";
  
    for (const result of results) {
        const row = document.createElement("tr");
        
        const uuidCell = document.createElement("td");
        uuidCell.textContent = result.uuid;
        row.appendChild(uuidCell);
        
        const jsonCell = document.createElement("td");
        const parsedJson = JSON.parse(result.json);
        jsonCell.textContent = JSON.stringify(parsedJson, null, 2);
        row.appendChild(jsonCell);
        
        tableBody.appendChild(row);
    }
}
  
