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

    formData.append(
        "file",
        fileInput.files[0]
    );

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

    document.getElementById(
    "status"
    ).innerText =
    data.message;

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

    const question =
    document.getElementById(
    "question"
    ).value;

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
                question:question
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
    data.context.join(
    "\n\n"
    );
}