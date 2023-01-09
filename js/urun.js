var sum=0;


products();



function products(){

  x = document.getElementsByClassName("1");

text="";
for(var i=0;i<x.length;i++){
  text=text+x[i].innerHTML+",";
}

var array = text.split(",");

array.pop();

sum=0;
for(var i=0;i<array.length;i++){
  sum=sum+parseInt(array[i]);
}

localStorage.setItem("sonuc",sum);
console.log(text);

document.getElementById("toplam").innerHTML="<div class='toplamınarkası '>Toplam Tutar: " + sum + " TL </div>" ;



  text2 = ""
var y= document.getElementById("urunler").children;

for(var i=0;i<y.length;i++){
  text2 = text2+"<section>"+y[i].innerHTML+ "</section>\n"
}

console.log(text2);
sessionStorage.setItem("urunler",text2)

}

function runme(e){
                //console.log(e.id);
                var elem=e.id;
                var k=document.getElementById(elem).parentElement.id;
                var l=document.getElementById(k).children[8].lastElementChild.id;
                console.log(l)
                var eksi = document.getElementById(l).innerHTML;
                console.log(eksi)
                console.log(parseInt(eksi))
                console.log(sum)
                sum=sum-parseInt(eksi)
                document.getElementById("toplam").innerHTML="<div class='toplamınarkası '>Toplam Tutar: " + sum + " TL </div>" ;
                console.log(sum)
                document.getElementById(k).remove();
                products();
        
            }