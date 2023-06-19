<script>


    let subministros = "";
    let demanda = "";

    let rows = [{id: 0, value: ""}]

    let file = "";

    let logs = "";

    function addRow(){
        rows.push({id: rows.length, value: ""})
        rows = rows;
    }

    async function callVoguel(fileStr) {
        try {
            const response = await fetch('http://localhost:8000/north-west?file_str=' + encodeURIComponent(fileStr));
            if (!response.ok) {
            throw new Error('Request failed with status: ' + response.status);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error calling /voguel:', error);
            throw error;
        }
    }


    function solve(){
        subministros = subministros.replace(/\s/g, '');
        demanda = demanda.replace(/\s/g, '');
        rows = rows.map(row => {
            row.value = row.value.replace(/\s/g, '');
            return row;
        })

        file = subministros + "\n" + demanda + "\n" + rows.map(row => row.value).join("\n");
        console.log(file);

//         file = `250,250,250,250
// 300,175,325,130,70
// 14,10,8,10,12
// 20,5,9,12,18
// 15,16,8,5,10
// 7,10,20,7,18`

        const apiUrl = 'http://localhost:8000/north-west';
        callVoguel(file)
        .then(result => {
            logs = result.result;

            // splitting logs in new lines
            logs = logs.split("\n");

            console.log('north-west API response:', result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
        }
</script>


<main>
    <h2>SUBMINISTROS</h2>
    <input class="i1" on type="text" bind:value={subministros} placeholder="Separados por comas...">

    <h2>DEMANDA</h2>      
    <input class="i1" on type="text" bind:value={demanda} placeholder="Separados por comas...">

    <h2>COLUMNAS</h2>      
    {#each rows as row (row.id)}
        <div class="twoinputs">
            <input class="i1" on type="text" bind:value={row.value} placeholder="Separados por comas...">
        </div>
    {/each}

    
    <div class="mas-container">
        <button on:click={() => addRow()} class="mas">+</button>
    </div>


    <div class="action-buttons">
        <button class="solve" on:click={() => solve()}>NOROESTE</button>
    </div>


    {#each logs as log}
        {#if log[0] == "["}
            <p style="font-weight: 900;">{log}</p>
            {#if log.includes("Coste optimo de transporte")}

                <h2 class="sol">{log}</h2>
            {/if}
        {:else}
            {#if log.includes("Table") || log.includes("Tabla")}
                <h2 class="tb">{log}</h2>
            {:else}
                <p>{log}</p>
            {/if}
        {/if}
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

    input{
        background-color: #f1f1f1;
        border: none;
        padding: 1em 2em;
        margin-top: 1em;
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

    .solve{
        background-color: #00FF90 !important;
        color: #004727;
        font-weight: 900;
    }

    .solve:hover{
        transform: scale(1.1);
    }

    .sol{
        background-color: #00FF90 !important;
        color: #004727;
        padding: 1em;
    }

    .tb{
        background-color: #f1f1f1;
        color: #454545;
        padding: 1em;
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
    animation: fadeInDelay 0.1s ease-in-out forwards;
    }

    /* Optional: Set initial opacity to 0 to ensure the delay effect */
    * {
    opacity: 0;
    }
</style>