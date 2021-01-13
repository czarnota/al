const API = "http://localhost:8000";

class Todo {
    // Saves wrapper, registers event handlers
    constructor(wrapper) {
        this.wrapper = wrapper;

        this.onFocusOut = this.onFocusOut.bind(this);
        this.wrapper.addEventListener("focusout", this.onFocusOut);

        this.items = [];
    }

    // Loads all todo list items from the backend and 
    // displays them
    async refresh() {
        const response = await fetch(API + "/todos/");

        this.items = await response.json();

        this.display();
    }

    // Get's called when inputs loose focus and
    // is responsible for adding, modyfing and deleting
    // todo list items
    async onFocusOut(event) {
        if (!event.target.matches('.todo-item'))
            return;

        if ("id" in event.target.dataset) {
            let id = event.target.dataset["id"];

            if (event.target.value) {
                await fetch(API + "/todos/edit/" + id, {
                    method: 'POST',
                    body: JSON.stringify({name: event.target.value}),
                    headers: { 'Content-Type': 'application/json' },
                })
            } else {
                await fetch(API + "/todos/delete/" + id, { method: 'POST' })
            }

            await this.refresh();
            return;
        }

        if (event.target.value) {
            await fetch(API + "/todos/create", {
                method: 'POST',
                body: JSON.stringify({name: event.target.value}),
                headers: { 'Content-Type': 'application/json' },
            })

            await this.refresh();
            return;
        }
    }

    // Builds HTML representation of the list
    display() {
        this.wrapper.innerHTML = `
            <h1>TODO</h1>
            <div>
                ${this.items.map(item => `<div><input class="todo-item" data-id="${item.id}" value="${item.name}" /></div>`).join("")}
                <div><input class="todo-item" value=""/></div>
            </div>
        `;
    }
}
