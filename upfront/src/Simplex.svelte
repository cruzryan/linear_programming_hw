<script>

    $: restricciones = [
        {
            id: 0,
            variables: "",
            final: "",

        }
    ];


    $: logs = []

    function addRestriction(){
        console.log("adding restriction");
        restricciones.push({
            id: restricciones.length,
            variables: "",
            final: "",
        })

        restricciones = restricciones;
        console.log(restricciones)
    }

    let max = false;

    let c = ""
    let b = ""
    let a = ""


    function solve(){
        console.log("solving...")

        for (let i = 0; i < restricciones.length; i++) {
            const restric = restricciones[i];
            a += restric.variables + ";"
        }
        
        a = a.substring(0, a.length - 1);

        for (let i = 0; i < restricciones.length; i++) {
            const restric = restricciones[i];
            b += restric.final + ","

        }

        b = b.substring(0, b.length - 1);

        console.log(a)
        console.log(b)
        console.log(c)

        console.log("Calling simplex:")

        callSimplex(a, b, c)
    }

    function callSimplex(a, b, c) {
        const url = 'http://localhost:8000/simplex';

        const params = new URLSearchParams({
            a: a,
            b: b,
            c: c
        });

        return fetch(`${url}?${params}`)
            .then(response => response.json())
            .then(data => {
            // Process the response data
            let tmplogs = JSON.parse(data);


            for(const key in tmplogs.logs){
                console.log(key)
                logs.push({
                    type: tmplogs.logs[key].type,
                    value: tmplogs.logs[key].value
                })
            }

            logs = logs;

            console.log(logs);
            })
            .catch(error => {
            // Handle any errors
            console.error(error);
            });
    }   

</script>


<main>
    
    <h2>FUNCIÓN OBJETIVO</h2>

    <div class="twoinputs">
        <input bind:value={c} class="i1" type="text" placeholder="Separados por comas...">
    </div>

    <h2>RESTRICCIONES</h2>

    {#each restricciones as restric (restric.id)}
        <div class="twoinputs">
            <input class="i1" on type="text" bind:value={restric.variables} placeholder="Separados por comas...">
            <input class="i2" type="text" bind:value={restric.final} placeholder="Final">
        </div>
    {/each}

    <div class="mas-container">
        <button on:click={() => addRestriction()} class="mas">+</button>
    </div>


    <div class="action-buttons">
        <button class="max" on:click={() => max = !max}>{max? "MAXIMIZAR" : "MINIMIZAR"}</button>
        <button class="solve" on:click={() => solve()}>SIMPLEX</button>
    </div>


    {#each logs as log}
        <div class="info">
            <h1>{log.type}</h1>
            {#if log.type === "table"}
    <table>
      <thead>
        <tr>
          {#each log.value[0] as header}
            <th>{header}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each log.value.slice(1) as row}
          <tr>
            {#each row as cell}
              <td>{Math.round(cell * 100) / 100}</td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  {:else}
    <div>{log.value}</div>
  {/if}
        </div>
    {/each}
    
</main>


<style>

    main{
        display: flex;
        flex-direction: column;
        align-items: start; 
        width: 33vw;
        margin-top: 2vh;
    }

    h2{
        font-size: 13px;
        margin-top: 2em;
    }

    .twoinputs{
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 1em;
    }
        
    input{
        background-color: #f1f1f1;
        border: none;
        padding: 1em 2em;
        
    }

    .i1{
        width: 50%;
    }

    .i2{
        width: 25%;
    }

    .mas{
        background-color: #f1f1f1;
        border: none;
        padding: 0.5em 1em;
        margin-top: 1em;
        cursor: pointer;
        user-select: none;
        font-size: 22px;
        color: #454545;
        border-radius: 5px;
    }

    .mas:hover{
        background-color: #e8e5e5;
    }

        
    .mas-container{
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 2vh;
    }


    .action-buttons{
        display: flex;
        width: 100%;
        justify-content: flex-end;
        align-items: center;
        margin-top: 2vh;
    }

    .action-buttons button{
        background-color: #f1f1f1;
        border: none;
        padding: 0.5em 1em;
        margin-top: 1em;
        cursor: pointer;
        user-select: none;
        font-size: 15px;
        color: #454545;
        margin-left: 1em;
    }

    .max{
        border: 1px solid black !important;
        background-color: transparent !important;
    }


    .solve{
        background-color: #00FF90 !important;
        color: #004727;
        font-weight: 900;
    }

    .solve:hover{
        transform: scale(1.1);
    }


    .info{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 5vh;
        margin-bottom: 5vh;
        border-top: 1px solid rgb(109, 109, 109);
    }

    .info h1{
        font-size: 15px;
        padding: 1em;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }
  
    th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    /* Define the keyframe animation */
    @keyframes fadeInDelay {
    0% {
        opacity: 0; /* Start with opacity 0 */
    }
    100% {
        opacity: 1; /* End with opacity 1 */
    }
    }

    /* Apply the animation to all elements */
    * {
    animation: fadeInDelay 0.2s ease-in-out forwards;
    }

    /* Optional: Set initial opacity to 0 to ensure the delay effect */
    * {
    opacity: 0;
    }

</style>