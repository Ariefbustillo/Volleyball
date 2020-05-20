    document.addEventListener('DOMContentLoaded', () => {

       document.querySelector('#rotate').onsubmit = () => {
           var player_one = document.querySelector('#playerOne').value;
           var player_six = document.querySelector('#playerSix').value;
           var player_five = document.querySelector('#playerFive').value;
           var player_two = document.querySelector('#playerTwo').value;
           var player_three = document.querySelector('#playerThree').value;
           var player_four = document.querySelector('#playerFour').value;

           var players = [player_one, player_two, player_three, player_four, player_five, player_six];
           for (i = 6;i < 12; i++){
               
               for (x = 0;x < 6; x++){
                   tables = document.querySelectorAll('table');

                   if (x === 0){
                       var table = tables[i - 6];
                       if (!table.rows[0]){
                            var row = table.insertRow(0);
                       }else{
                           var row = table.rows[0];
                       }
                   }
                   if (x < 3){
                       if (!table.rows[0].cells[x]){
                            var cell = row.insertCell(x);
                       } else{
                           var cell = table.rows[0].cells[x];
                       }
                       cell.innerHTML = players[(i - x) % 6];
                       
                   } else {
                       if (!table.rows[1]){
                           var row = table.insertRow(1);
                           if (!table.rows[1].cells[1]){
                                row.insertCell(0);
                                row.insertCell(1);
                                row.insertCell(2);
                           }
                       }    
                        var cell = table.rows[1].cells[5-x];
                        cell.innerHTML = players[(i - x) % 6];
                   }
                   
               }
           }

           event.returnValue = false;
           
               

           };
       });