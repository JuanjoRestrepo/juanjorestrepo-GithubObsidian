


**Selecciona film_id y imdb_score en la tabla reviews y filtra por puntuaciones superiores a 7,0.** 
```sql 
SELECT film_id, imdb_score FROM reviews WHERE imdb_score > 7.0; 
```

**Selecciona film_id y facebook_likes de los diez primeros registros con menos de 1000 me gusta en la tabla reviews.**
```sql 
SELECT film_id, facebook_likes FROM reviews WHERE facebook_likes < 1000 LIMIT 10; 
``` 

**Cuenta cuántos registros tienen un num_votes mínimo de 100 000; utiliza el alias films_over_100K_votes.** 
```sql 
SELECT COUNT(*) AS films_over_100K_votes FROM reviews WHERE num_votes >= 100000; 
```



