const button = document.getElementById("submit");
const form = document.getElementById("form");
let count = 1;
const newTextIn = () => {
    const textbox = document.createElement("textarea");
    textbox.setAttribute("placeholder", "Write your message here");
    textbox.setAttribute("maxlength","2000");
    textbox.setAttribute("id", `${count}`);
    textbox.setAttribute("name", `text${count}`);
    textbox.classList.add('Textbox');
    form.insertBefore(textbox, button);
    const inbox = document.createElement("input");
    inbox.setAttribute("type", "text");
    inbox.setAttribute("placeholder", "User input");
    inbox.setAttribute("id", `${count}`);
    inbox.setAttribute("readonly","true");
    inbox.setAttribute("maxlength","30");
    inbox.classList.add('Inputbox');
    form.insertBefore(inbox, button);
    count++;
    const email = document.createElement("input");
    email.setAttribute("type", "email");
    email.setAttribute("placeholder", "User Email");
    email.setAttribute("required", "true");
    email.setAttribute("id", `${count}`);
    email.setAttribute("name", `email${count}`);
    email.setAttribute("maxlength","30");
    email.classList.add('Inputbox');
    count++;
    form.append(email, button);
}
const newText = () => {
    const textbox = document.createElement("textarea");
    textbox.setAttribute("placeholder", "Write your message here");
    textbox.setAttribute("maxlength","2000");
    textbox.setAttribute("id", `${count}`);
    textbox.setAttribute("name", `textbox${count}`);
    textbox.classList.add('Textbox');
    count++;
    form.insertBefore(textbox, button);
}