let count = 1;
const newTextIn = () => {
    const textbox = document.createElement("input");
    textbox.setAttribute("type", "text");
    textbox.setAttribute("placeholder", "User input");
    textbox.setAttribute("id", `${count}`);
    textbox.setAttribute("readonly","true");
    textbox.setAttribute("maxlength","30");
    textbox.classList.add('Inputbox');
    count++;
    document.getElementsByClassName("text-cont")[0].appendChild(textbox);
}
const newText = () => {
    const textbox = document.createElement("textarea");
    textbox.setAttribute("placeholder", "Write your message here");
    textbox.setAttribute("maxlength","2000");
    textbox.setAttribute("id", `${count}`);
    textbox.classList.add('Textbox');
    count++;
    document.getElementsByClassName("text-cont")[0].appendChild(textbox);
}
const submit = () => {
    console.log("This should submit the template but I don't know how")
}