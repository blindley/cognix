
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


function initFixedFields() {
    addRow(true, 'cognix.cardTemplate', 'cognix.basic', true);
    addRow(false, 'cognix.instanceCount', 1, true);
}

function validateKey(input) {
    const keys = document.getElementsByClassName("key");
    for (let i = 0; i < keys.length; i++) {
        if (keys[i] !== input && keys[i].value === input.value) {
            alert("Duplicate keys are not allowed!");
            input.setCustomValidity("Duplicate keys are not allowed!");
            return;
        }
    }
    input.setCustomValidity("");
}

function deleteRow(node) {
    row = findAncestorWithClass(node, "fieldRow");
    row.parentNode.removeChild(row);
}

function addRow(focus = false, keyName = null, value = null, fixedKey = false) {
    const table = document.getElementById("cardDataTable");
    const row = table.insertRow(-1);
    row.classList.add('fieldRow');

    const keyCell = row.insertCell(0);
    const valueCell = row.insertCell(1);
    const actionCell = row.insertCell(2);

    const keyInput = document.createElement('input');
    keyInput.type = 'text';
    keyInput.className = 'key';
    keyInput.disabled = fixedKey;
    keyInput.onblur = () => validateKey(keyInput);
    keyInput.onkeydown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const nextValueInput = e.target.parentNode.nextElementSibling.firstElementChild;
            nextValueInput.focus();
        }
    };

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
    keyCheckbox.className = 'key-checkbox';
    keyCheckbox.disabled = fixedKey;
    keyCheckbox.onchange = () => {
        if (!keyCheckbox.checked) {
            valueCheckbox.checked = false;
        }
    };

    const valueCheckbox = document.createElement('input');
    valueCheckbox.type = 'checkbox';
    valueCheckbox.className = 'value-checkbox';
    valueCheckbox.disabled = fixedKey;
    valueCheckbox.onchange = () => {
        if (valueCheckbox.checked) {
            keyCheckbox.checked = true;
        }
    };

    if (!fixedKey) {
        keyCell.prepend(keyCheckbox);
        valueCell.prepend(valueCheckbox);
        actionCell.innerHTML = '<button onclick="deleteRow(this)">Delete</button>';
    }

    keyInput.value = keyName || '';
    valueInput.value = value || '';

    keyCell.appendChild(keyInput);
    valueCell.appendChild(valueInput);

    if (focus) {
        keyInput.focus();
    }
}

function resetFields() {
    const table = document.getElementById("cardDataTable");

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
    const json = {};
    const keys = document.getElementsByClassName("key");
    const values = document.getElementsByClassName("value");

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i].value;
        let value = values[i].value;

        try {
            value = JSON.parse(value);
        } catch (e) {
            const lowerCase = value.toLowerCase();
            if (lowerCase === 'true') {
                value = true;
            } else if (lowerCase === 'false') {
                value = false;
            } else if (lowerCase == 'null' || lowerCase == 'none') {
                value = null;
            } else {
                // Leave value as string
            }
        }

        json[key] = value;
    }

    const response = await fetch('/process-card-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    });

    if (response.ok) {
        const result = await response.json();
        if (result.success) {
            document.getElementById("result").innerText = "Card data processed successfully!";
            resetFields(); // Add this line to reset the fields
        } else {
            const errors = result.errors.join("\n");
            document.getElementById("result").innerText = `Error processing Card data:\n${errors}`;
        }
    } else {
        document.getElementById("result").innerText = "Error sending Card data.";
    }
}
