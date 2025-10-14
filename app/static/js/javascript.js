async function registerFunc(event) {
    event.preventDefault();

    const form = document.getElementById('register_form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/auth/register", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            displayErrors(errorData);
            return;
        }

        const result = await response.json();

        if (result.message) {
            window.location.href = "/auth/login/view";
        } else {
            alert(result.message || 'Неизвестная ошибка');
        }
    } catch (err) {
        console.log("ошибка:", err);
        alert("Произошла ошибка, попробуйте снова");
    }
}


async function loginHandler(event) {
    try {
        event.preventDefault();

        const form = document.getElementById("login_form");
        const formData = new FormData(form);
        const formDataObj = Object.fromEntries(formData.entries());
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formDataObj)
        });

        if (!response.ok) {
            const errors = await response.json();
            return;
        }

        const result = await response.json();
        if (result.message) {
            window.location.href = "/auth/me";
        } else {
            alert("Произошла ошибка, попробуйте снова");
        }

    } catch (err) {
        console.log("Ошибка", err);
        alert("Произошла ошибка, попробуйте снова");
    }
}

async function registerPage(event) {
  event.preventDefault();

  try {
      window.location.href = "/auth/register/view";
  }catch(err) {
     console.log("Ошбка", err)
     alert("Вы не можете зарегистрироваться в данный момент, пожалуйста попробуйте позже.")
  }
}


async function logOut(event) {
  event.preventDefault();

  try {
    const response = await fetch("/auth/logout", {
      method: "POST",
      credentials: "include", // обязательно, чтобы куки отправились
    });

    const result = await response.json();

    if (!response.ok) {
      displayErrors(result);
      return;
    }

    if (result.message) {
      window.location.href = "/auth/register/view";
    } else {
      alert("Произошла ошибка при выходе");
    }
  } catch (error) {
    console.error("Ошибка при запросе logout:", error);
    alert("Ошибка. Попробуйте снова.");
  }
}

async function roofForm(event) {
    event.preventDefault();


    const formContainer = document.getElementById("roofFForm")
    const answerContainer = document.getElementById("roofSForm")
    const ownBlock = document.querySelector(".own-block")

    answerContainer.innerHTML = ""
    formContainer.innerHTML = ""

    formContainer.style.width = "41%"
    answerContainer.style.width = "60%"
    ownBlock.style.height = "100%"



         const form = {
              "Пролет стропила": "L, м",
              "Ширина стропила": "b, мм",
              "Высота стропила": "h, мм",
              "Снеговая нагрузка": "q_s, кг/м²",
              "Вес кровли (металлочерепица)": "g_k, кг/м²",
              "Вес обрешетки/утеплителя": "g_u, кг/м²",
              "Ветровая нагрузка": "q_w, кг/м²",
              "Допуст напряжение для дерева": "q_dop, МПа",
              "Модуль упругости дерева": "E, МПа",
};




    for (let label in form) {
        const fieldName = form[label];

        const wrapper = document.createElement("fieldset");
        wrapper.className = "field-descr";
        wrapper.style.width = "90%"

        const lbl = document.createElement("legend");
        lbl.className = "lgd-cont";
        lbl.textContent = label + " " + "(" + fieldName + ")";

        const input = document.createElement("input");
        input.className = "inp-t-desk";
        input.type = "text";
        input.name = fieldName.split(",")[0];
        input.required = true;
        input.style.width = "100%"

        wrapper.appendChild(lbl);
        wrapper.appendChild(input);
        formContainer.appendChild(wrapper);}
    const button = document.createElement("button");
    button.type = "submit";
    button.textContent = "Отправить";
    button.onclick = getAnswer;
    formContainer.appendChild(button);

    const answerWrapper  = document.createElement("fieldset");
    answerWrapper.style.width = "50%";
    answerWrapper.style.height = "100%";
    answerWrapper.className = "field-set";

    const legend = document.createElement("legend");
    legend.className = "ldg-cont-2";
    legend.textContent = "Answer";

    const p = document.createElement("p");
    p.style.height = "100%";
    p.style.width = "50%";
    p.id = "first-par";

    answerWrapper.appendChild(legend);
    answerWrapper.appendChild(p);
    answerContainer.appendChild(answerWrapper);
}


async function getAnswer(event) {
     event.preventDefault();

     const field_set_margin_top = document.querySelector(".field-set");


     try{
     const form = document.getElementById("roofFForm");
     const data = new FormData(form);
     const result = Object.fromEntries(data.entries());

     const response = await fetch("/calcul/load_o_the_roof", {
                     method: "POST",
                     headers: {'Content-Type': 'application/json'},
                     body: JSON.stringify(result)
                     });


     if (!response.ok) {
         alert("Вы можете отправить только полностью заполненую форму");
         return;}

     field_set_margin_top.style.marginTop = "10px";
     const res = await response.json();

     if (res.message) {
          document.getElementById("first-par").innerHTML = res.message;
          }
     else{
         alert("Произошла ошибка при отправке ответа, попробуйте сново позже");
         return;
     }
     } catch(err) {
         console.log("Произошла ошибка", err);
         alert("Произошла ошибка, попробуйте позже");
         return;
         }
     }