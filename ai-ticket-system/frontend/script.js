// Create Ticket (POST)
async function createTicket() {
    const text = document.getElementById("ticketText").value;

    if (!text) {
        alert("Please enter some text");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/ticket", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        alert("Ticket Created ✅");

        // Clear input
        document.getElementById("ticketText").value = "";

        // Refresh ticket list
        getTickets();

    } catch (error) {
        console.error(error);
        alert("Error connecting to server ❌");
    }
}


// Get All Tickets (GET)
async function getTickets() {
    try {
        const response = await fetch("http://127.0.0.1:8000/tickets");
        const data = await response.json();

        const list = document.getElementById("ticketList");
        list.innerHTML = "";

        data.forEach(ticket => {
            const li = document.createElement("li");
            li.textContent = `#${ticket.id} | ${ticket.text} | ${ticket.category} | ${ticket.status}`;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Error loading tickets ❌");
    }
}


// Load tickets when page opens
window.onload = function () {
    getTickets();
};
function showPage(page) {
    const content = document.getElementById("contentArea");

    if (page === "dashboard") {
        content.innerHTML = "<h2>Welcome to Ticket System</h2>";
    }

    else if (page === "new") {
        content.innerHTML = `
            <h2>Create Ticket</h2>
            <input type="text" id="ticketText" placeholder="Enter issue">
            <button onclick="createTicket()">Submit</button>
        `;
    }

    else if (page === "tickets") {
        content.innerHTML = `
            <h2>All Tickets</h2>
            <ul id="ticketList"></ul>
        `;
        getTickets();
    }
}