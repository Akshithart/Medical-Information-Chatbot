async function uploadPDF() {

    const fileInput =
        document.getElementById("pdfFile");

    if (!fileInput.files.length) {

        alert("Please select a PDF");

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    const response =
        await fetch("/upload", {
            method: "POST",
            body: formData
        });

    const data =
        await response.json();

    document.getElementById(
        "status"
    ).innerText =
        data.message;

    alert(data.message);
}



async function askQuestion() {

    const question =
        document.getElementById(
            "question"
        ).value;

    const response =
        await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

    const data =
        await response.json();

    document.getElementById(
        "answer"
    ).innerText =
        data.answer;
}