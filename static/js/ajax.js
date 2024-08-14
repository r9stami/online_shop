



 // $("#comment_form").on('submit', function(event) {
 //       event.preventDefault();
 //       var message = document.getElementById('message');
 //       var name = document.getElementById('name');
 //       var email = document.getElementById('email');
 //       var phone = document.getElementById('phone');
 //       $.ajax({
 //           type: "POST",
 //           url: `/product/comment}`,
 //           data:{
 //                 message:message,
 //                 name:name,
 //                 email:email,
 //                 phone:phone,
 //                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
 //           },
 //           datatype:'json',
 //           success: function(data) {
 //             if (data['success'])
 //                alert("successfully added to favorites")
 //           }
 //       });
 //  });


function like(slug,pk) {
    $.get(`/product/like/${slug}/${pk}`).then(response =>{
        var element = document.getElementById('like')
        var count =document.getElementById('count_like')

        if (response['response']==='like'){
         element.className = 'fa fa-heart'
         count.innerText = Number(count.innerText) + 1


        }else{
            element.className = 'far fa-heart'
            count.innerText = Number(count.innerText) - 1
        }
       })


}


// function comment(pk){
//     $.post(`/product/comment/${pk}`).then(response =>{
//         var message = document.getElementById('message_c')
//         var email = document.getElementById('email_c')
//
//         if(response['response'] === 'comment'){
//             $.ajax({
//                 type: 'POST',
//                 url: `product/comment/${pk}`,
//                 data: {
//                     message:message,
//                     email:email
//                 }
//
//             })
//         }
//
//
//     })
// }