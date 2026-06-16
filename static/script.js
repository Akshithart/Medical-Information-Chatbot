async function uploadPDF() {

    const fileInput =
    document.getElementById(
    "pdfFile"
    );

    if(
        !fileInput.files.length
    ){
        alert(
        "Select a PDF"
        );
        return;
    }

    const formData =
    new FormData();

    for(let i = 0; i < fileInput.files.length; i++){
    formData.append(
        "files",
        fileInput.files[i]
    );
}

    const response =
    await fetch(
        "/upload",
        {
            method:"POST",
            body:formData
        }
    );

    const data =
    await response.json();

    if(data.context){

    document.getElementById(
        "context"
    ).innerText =
    data.context;
    }
    if(
        data.message
    ){
        setTimeout(
            ()=>{
                window.location.href=
                "/chatpage";
            },
            1500
        );
    }
}



async function askQuestion(){

    const loader =
    document.getElementById(
        "loader"
    );

    const downloadBtn =
    document.getElementById(
        "downloadBtn"
    );

    loader.style.display =
    "block";

    try{

        const question =
        document.getElementById(
            "question"
        ).value.trim();

        if(!question){

            alert(
                "Please enter a question"
            );

            return;
        }

        const response =
        await fetch(
            "/chat",
            {
                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({
                    question
                })
            }
        );

        const data =
        await response.json();

        document.getElementById(
            "answer"
        ).innerText =
        data.answer;

        document.getElementById(
            "context"
        ).innerText =
        data.context;

        if(downloadBtn){

            downloadBtn.style.display =
            "inline-block";
        }

        loadHistory();

    }catch(error){

        console.error(
            error
        );

        alert(
            "Error generating answer"
        );

    }finally{

        loader.style.display =
        "none";
    }
}
async function loadHistory(){

    const response =
    await fetch(
        "/history"
    );

    const data =
    await response.json();

    const historyList =
    document.getElementById(
        "historyList"
    );

    historyList.innerHTML =
    "";

    data.forEach(
        (item)=>{

            const li =
            document.createElement(
                "li"
            );

            li.innerText =
            item.question;

            li.onclick = ()=>{

    document.getElementById(
        "question"
    ).value =
    item.question;

    document.getElementById(
        "answer"
    ).innerText =
    item.answer;

    document.getElementById(
        "context"
    ).innerText =
    item.context;
};

            historyList.appendChild(
                li
            );
        }
    );
}

window.onload =
loadHistory;
document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        const questionBox =
        document.getElementById(
            "question"
        );

        if(questionBox){

            questionBox.addEventListener(
                "keypress",
                function(e){

                    if(e.key==="Enter"){

                        askQuestion();
                    }
                }
            );
        }
    }
);

async function clearHistory(){

    await fetch(
        "/clear-history",
        {
            method:"POST"
        }
    );

    loadHistory();

    document.getElementById(
        "answer"
    ).innerHTML="";

    document.getElementById(
        "context"
    ).innerHTML="";
}

async function downloadReport(){

    const question =
    document.getElementById(
        "question"
    ).value;

    const context =
    document.getElementById(
        "context"
    ).innerText;

    const answer =
    document.getElementById(
        "answer"
    ).innerText;

    if(!answer){

        alert(
            "No answer available."
        );

        return;
    }

    const response =
    await fetch(
        "/download-report",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                question:
                question,

                context:
                context,

                answer:
                answer

            })
        }
    );

    const data =
    await response.json();

    window.open(
        data.pdf,
        "_blank"
    );
}

document.addEventListener(
    "DOMContentLoaded",
    ()=>{

        const questionBox =
        document.getElementById(
            "question"
        );

        if(questionBox){

            questionBox.addEventListener(
                "keypress",
                function(e){

                    if(
                        e.key === "Enter"
                    ){
                        askQuestion();
                    }
                }
            );
        }
    }
);