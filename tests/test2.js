let number x;  /* global*/
x = 3;
function number factorial(number x)
/* se define la función recursiva con un parámetro, 
   que oculta a la variable global de igual nombre */
{
    if (x == 1) x++;
    x = x++;


}	/* la función devuelve un entero*/
function boolean Suma(number aux, number fin)
/* se define la función Suma que recibe 
   dos enteros por valor */
/* usa la variable global x */
{
    aux = factorial(aux - 1);

    return aux != 10000;
}	/* la función devuelve un lógico*/
function Imprime(number a) {
    alert(a);
    return a;	/* esta instrucción se podría omitir*/
}	/* la función no devuelve nada*/

do {
    x++;
    alert(x);

} while (x != 5);
Imprime(factorial(Suma(5, 3)));	/* se llama a las tres funciones*/