<script>
    import Noroeste from "./Noroeste.svelte";
    import Simplex from "./Simplex.svelte";
    import Vogel from "./Vogel.svelte";


	let selected = 'noroeste'; // simplex, vogel, noroeste

</script>

<main>

	<div class="nav">
		<h2 on:click={() => selected = "simplex"} class={selected == "simplex"? "selected" : ""}>SIMPLEX</h2>
		<h2 on:click={() => selected = "noroeste"} class={selected == "noroeste"? "selected" : ""}>NOROESTE</h2>
		<h2 on:click={() => selected = "vogel"} class={selected == "vogel"? "selected" : ""}>VOGEL</h2>
	</div>

	{#if selected == "simplex"}
		<Simplex />
	{/if}

	{#if selected == "vogel"}
		<Vogel />
	{/if}

	{#if selected == "noroeste"}
		<Noroeste />
	{/if}

</main>

<style>

	main {
		width: 100vw;
		height: 100vh;
		display: flex;
		align-items: center;
		flex-direction: column;
	}
	
	.nav {
		display: flex;
		justify-content: space-around;
		align-items: center;
		
		height: 50px;
		width: 33vw;

		margin-top: 10vh;
		border-bottom: 1px solid #a3a3a3;
	}

	.nav h2 {
		font-size: 15px;
		color: #a3a3a3;
		cursor: pointer;
		user-select: none;

	}

	.selected {
		color: #383838 !important;
	}

</style>