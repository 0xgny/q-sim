/ feed.q - Generates simulated market data
\l schema.q

/ Connect to Tickerplant
tph:hopen `::5010

syms:`AAPL`MSFT`GOOG`TSLA;

/ Generate random trades and quotes
generate_trade:{[]
    n:10; / 10 trades per tick
    t:n#.z.n;
    s:n?syms;
    p:100.0 + n?50.0;
    sz:10 * 1 + n?100;
    tph(`.u.upd; `trade; (t;s;p;sz));
 }

generate_quote:{[]
    n:10;
    t:n#.z.n;
    s:n?syms;
    b:100.0 + n?50.0;
    a:b + 0.01 + n?0.10;
    bsz:100 * 1 + n?10;
    asz:100 * 1 + n?10;
    tph(`.u.upd; `quote; (t;s;b;a;bsz;asz));
 }

/ Timer function triggered every X milliseconds
.z.ts:{
    generate_trade[];
    generate_quote[];
 }

/ Start generating data every 500ms
\t 500
show "Feedhandler started."
