const job_form = document.querySelector(".job_form"),
    job_input = job_form.querySelector("input"),
    history = document.querySelector(".list");
    
const loading = document.querySelector(".loading");
const historyList = "history";
let inputHistory = [];

function saveHisotry() {
  localStorage.setItem(historyList,JSON.stringify(inputHistory));
}

function delHistory(event) {
  const btn = event.target;
  const li = btn.parentNode;
  history.removeChild(li);
  const cleanHistory = inputHistory.filter(function(his){
    console.log(li.id, his.id);
    return his.id !== parseInt(li.id);
  })
  inputHistory = cleanHistory;
  saveHisotry();

}

function displayHistory(text){
  const li = document.createElement("div");
  const delBtn = document.createElement("button");
  const anchor = document.createElement("a");
  const newId = inputHistory.length + 1;
  anchor.href = "/detail?job=" + text;
  anchor.innerHTML = text;
  delBtn.innerHTML = "❌";
  delBtn.addEventListener("click",delHistory);
  anchor.addEventListener("click", ()=> {
    console.log("anchor click")
    loading.style.visibility='visible';
})
  li.appendChild(anchor);
  li.appendChild(delBtn);
  li.id = newId;
  history.appendChild(li);
  const historyObj = {
    text:text,
    id:newId
  };
  inputHistory.push(historyObj);
  saveHisotry();
  console.log("displayHistory")
  // job_form.submit();
}

function handleHistory(event) {
  event.preventDefault();
  job_form.submit();
  loading.style.visibility='visible';
  console.log("visible")
  const currentValue = job_input.value;
  var i;
  for (i = 0; i < inputHistory.length; i++){
    var bool = inputHistory[i].text.includes(currentValue);
    if (bool === true) {
      job_input.value = "";
      console.log(inputHistory[i].text)
      console.log("same")
      return
    }
    
  }
  displayHistory(currentValue);
  job_input.value = "";
  // loading.style.visibility='hidden';
  console.log("hidden")
}

function loadList() {
  const loadedHistory = localStorage.getItem(historyList);
  if (loadedHistory !== null){
    const parsedHistory = JSON.parse(loadedHistory);
    parsedHistory.forEach(function(eachHistory) {
      displayHistory(eachHistory.text);
    });
  }
}


function init() {
  job_form.addEventListener("submit",handleHistory);
  loadList();
}

init();

// 로딩화면 띄울때 요 코드 참고해서 구현해볼것. window.addEventListener("load", setTimeout(function(){ /* stuff */}, 3000));