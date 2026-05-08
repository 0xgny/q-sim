/ tp.q - Lightweight pub/sub router
\p 5010
\l schema.q

/ Dictionary to map table names to subscriber handles
subscribers:()!()

/ The update function called by the feedhandler
.u.upd:{[t;data]
    / Publish the data to all subscribers of table 't'
    if[count subscribers[t];
        {[h;t;data] (neg h)(`.u.upd;t;data)}[;t;data] each subscribers[t]
    ];
 }

/ The subscribe function called by the RDB
.u.sub:{[t]
    subscribers[t]:distinct subscribers[t],.z.w;
    show "Handle ",(string .z.w)," subscribed to ",(string t);
 }
