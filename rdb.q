/ rdb.q - In-memory store and query engine
\p 5011
\l schema.q

/ Connect to the Tickerplant
tph:hopen `::5010

/ Define the update function to insert incoming data into local tables
.u.upd:{[t;data]
    t insert data;
 }

/ Subscribe to both tables
tph(`.u.sub;`trade);
tph(`.u.sub;`quote);

show "RDB initialized and subscribed to Tickerplant."
