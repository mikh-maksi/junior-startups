right_answer_n = 0;

k = Number(n_question.value);
console.log(k);
n.innerHTML=k+1;
n_right.innerHTML=right_answer_n;
point = 1;

answers(n_question.value);

get_answer.addEventListener("click", f_get_answer);
view_answer.addEventListener("click", f_view_answer);
next_question.addEventListener("click", f_next_question);

  function f_get_answer (){

    if (y1.checked){ n_a = 1;}
    if (y2.checked){ n_a = 2;}
    if (y3.checked){ n_a = 3;}
    if (y4.checked){ n_a = 4;}

    if (n_a == n_right_answer){
      right_div.classList.remove("hidden");
      wrong_div.classList.add("hidden");
      right_answer_n = right_answer_n +point;
      point = 0;
    }else{
      right_div.classList.add("hidden");
      wrong_div.classList.remove("hidden");
      point = 0;
    }
   
  }
  function f_view_answer (){
    answer.classList.toggle("hidden");
    view_answer.classList.toggle("opend");
  }
  function f_next_question (){
    if (k<Number(n_question.value)-1){
    console.log(k,Number(n_question.value));
    right_div.classList.add("hidden");
    answer.classList.add("hidden");
    point = 1;
    k+=1;
    n_right.innerHTML=right_answer_n;
    n.innerHTML=k+1;
    answers(k);
    }else{
      n_right.innerHTML=right_answer_n;

      wrapper.innerHTML='';
    }
  }

function answers(k){
  query = 'https://innovations.kh.ua/quiz/list/?author_id=0&n='+k;
  console.log(query);
  fetch(query).then(response => response.json())
  .then(function (quiz) {
    question.innerHTML=quiz.question_arr[0];
    title.innerHTML = quiz.title_arr[0];
    a1.innerHTML = quiz.a1_arr[0];
    a2.innerHTML = quiz.a2_arr[0];
    a3.innerHTML = quiz.a3_arr[0];
    a4.innerHTML = quiz.a4_arr[0];
    answer.innerHTML = quiz.answer_arr[0];
    
    n_right_answer = quiz.n_right_answer_arr[0];
    n_question.value = quiz.total_n;
    console.log(quiz);
      
  });
}
