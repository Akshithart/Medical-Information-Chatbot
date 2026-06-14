async function askQuestion(){

let question =
document.getElementById(
"question"
).value;

let response =
await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:JSON.stringify({
question:question
})

});

let data=
await response.json();

document.getElementById(
"answer"
).innerHTML=
data.answer;
}
