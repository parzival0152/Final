const button = document.getElementById("submit");
const form = document.getElementById("form");
let count = 1;
let stCount = 1;
const newIn = () => {
    // const textbox = document.createElement("textarea");
    // textbox.setAttribute("placeholder", "Write your message here");
    // textbox.setAttribute("maxlength","2000");
    // textbox.setAttribute("id", `${count}`);
    // textbox.setAttribute("name", `text${count}`);
    // textbox.classList.add('Textbox');
    // form.insertBefore(textbox, button);
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

const newStation = () => {
    const newSt = document.createElement("div");
    newSt.setAttribute("id", `${stCount}`);
    newSt.setAttribute("name", `section${stCount}`);
    form.insertBefore(newSt, button);

    const dropdwn = document.createElement("div");
    newSt.setAttribute("name", `drpdiv${stCount}`);
    dropdwn.classList.add("dropdown");
    newSt.appendChild(dropdwn);

    const createSecBtn = document.createElement("button");
    createSecBtn.setAttribute("id", `sectionbtn${stCount}`);
    createSecBtn.innerHTML = "Create new section";
    createSecBtn.setAttribute("name", `sectionbtn${stCount}`);
    createSecBtn.classList.add('dropbtn');
    dropdwn.appendChild(createSecBtn);

    const drpcont = document.createElement("div");
    newSt.setAttribute("name", `drpcont${stCount}`);
    drpcont.classList.add('dropdown-content');
    dropdwn.appendChild(drpcont);

    const createTxt = document.createElement("button");
    createTxt.setAttribute("id", `createTxt${stCount}`);
    createTxt.innerHTML = "Add text section";
    createTxt.setAttribute("name", `createTxt${stCount}`);
    createTxt.setAttribute("onclick", "newText()");
    createTxt.classList.add('optionbtn');
    drpcont.appendChild(createTxt);

    const createIn = document.createElement("button");
    createIn.setAttribute("id", `createIn${stCount}`);
    createIn.innerHTML = "Add text section";
    createIn.setAttribute("name", `createIn${stCount}`);
    createIn.setAttribute("onclick", "newIn()");
    createIn.classList.add('optionbtn');
    drpcont.appendChild(createIn);

    stCount++;
}