const form = document.getElementById("process-form");
const inputArea = document.getElementById("input-area");
var i = 0;

function addRow() {
    i++;
    const newInput = document.createElement("div");
    newInput.innerHTML = `
        process ${i}: 
        <input type="text" placeholder="Arrival time" name="at" required>
        <input type="number" placeholder="Burst Time" name="bt" required>
    `;
    inputArea.appendChild(newInput);
}

function removeRow() {
    if (i > 0) {
        inputArea.removeChild(inputArea.lastChild);
        i--;
    } else {
        alert("At least one process is required.");
    }
}   


function clearRows() {
    const inputs = inputArea.querySelectorAll("div");
    inputs.forEach(input => {
        inputArea.removeChild(input);
    });
    i=0;
}   


form.onsubmit = async function(e) {
    e.preventDefault();
    const inputs = inputArea.querySelectorAll("div");
    
    if (inputs.length === 0) {
        alert("Please add at least one process.");
        return;
    }
    
    const processes = [];
     let hasError = false;
    inputArea.querySelectorAll("div").forEach((div, index) => {
        const [at, bt] = div.querySelectorAll("input");
        if (bt.value === "0") {
            alert("Burst time cannot be zero");
            bt.focus();
            bt.style.border = "3px solid red";
            hasError = true;
             
            bt.addEventListener("input", function handler() {
                if (bt.value !== "0") {
                    bt.style.border = "";
                    bt.removeEventListener("input", handler); // Remove after fixing
                }
            });

            return;
        }
        processes.push({
            pid: index + 1,
            at: at.value,
            bt: bt.value
        });
    });
    
    if (hasError) return;

    console.log("processes", processes);
    const res = await fetch("/simulate/srtf", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ processes })
    });
    
    console.log("res");
    if (!res.ok) {
        alert("Error: " + res.statusText);
        return;
    }

    const data = await res.json();
    animateChart(data.scheduled);
    renderTable(data.table, data.average_waiting_time, data.average_turnaround_time);
}

function animateChart(scheduled) {
    const chart = document.getElementById("gantt-chart");
    const inner=document.createElement("div");
    inner.className = "gantt-inner";
    chart.innerHTML = "";
    
    const heading = document.createElement("h3");
    heading.innerText = "GANTT CHART";
    heading.style.textAlign = "center";
    heading.style.color = "blue";   
    chart.appendChild(heading);

    scheduled.forEach((p, index) => {
        setTimeout(() => {
            const block = document.createElement("div");
            block.className = "process-block";
            //block.style.width = (40) + "px";
            block.style.width ='3px';
            if(p=="idle"){
                block.style.backgroundColor = "#2ecc71";
                block.innerText = "idle";
            }
            else{
                block.style.backgroundColor = "#3498db";
                block.innerText = `p${p}`;
            }
            //block.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
           // block.style.backgroundColor = "#3498db";
            // block.innerHTML = `<p>P ${p.pid}</p>
            //            <p>(${p.starting_time} - ${p.completion_time})</p>`;
            inner.appendChild(block);
                    
        }, index * 1000);
        });
        chart.appendChild(inner);
}

function renderTable(tableData, avgWT, avgTAT) {
    const tableContainer = document.getElementById("process-table");
    tableContainer.innerHTML = "";  // Clear previous table
    
    const heading = document.createElement("h3");
    heading.innerText = "PPOCESS SCHEDULING TABLE";
    heading.style.textAlign = "center";
    heading.style.color = "blue";
    tableContainer.appendChild(heading);

    const table = document.createElement("table");
    table.border = "1";
    table.style.borderCollapse = "collapse";

    // Create header
    const header = document.createElement("tr");
    ["PID", "AT", "BT", "Start", "CT", "WT", "TAT", "RT"].forEach(text => {
        const th = document.createElement("th");
        th.innerText = text;
        th.style.padding = "5px";
        header.appendChild(th);
    });
    table.appendChild(header);

    // Create rows
    tableData.forEach(p => {
        const row = document.createElement("tr");
        ['p'+p.pid, p.arrival_time, p.burst_time, p.starting_time, p.completion_time, p.waiting_time, p.turnaround_time, p.response_time]
            .forEach(val => {
                const td = document.createElement("td");
                td.innerText = val;
                td.style.padding = "5px";
                row.appendChild(td);
            });
        table.appendChild(row);
    });

     tableContainer.appendChild(table);
    // Add averages row
    const avg = document.createElement("div");
    avg.innerHTML = `<div>
               <p>average waiting time: <strong>${avgWT}</strong> </p>
               <p>average turnaround time: <strong>${avgTAT}</strong> </p>
               <p>average response time: <strong>${avgWT}</strong> </p>
           </div>`;
    tableContainer.appendChild(avg);
}

