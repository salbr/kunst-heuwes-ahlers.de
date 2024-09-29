<script>
	import { Label, Input } from 'flowbite-svelte';

    function handleOnSubmit(event) {
        event.preventDefault();
        const name = event.target.name.value;
        const email = event.target.email.value;
        const message = event.target.message.value;
        console.log(name, email, message);
    }
</script>

<svelte:head>
	<title>Kontakt - Ruth Heuwes-Ahlers</title>
	<meta name="description" content="Kontakt zu Ruth Heuwes-Ahlers" />
</svelte:head>
<div class="main">
	<div class="contactDescription">
		<h1>SCHREIBEN SIE MIR.</h1>
		<p>
			Sie können mich unter folgenden Kontaktdaten erreichen, oder nutzen Sie das
			Formular.
		</p>
		<h4>Ruth Heuwes-Ahlers</h4>
		<p>
			Fon: 05231/3012010 <br />
			Email: info@kunst-heuwes-ahlers.de
		</p>
	</div>
	<div class="contactForm">
		<form action="https://api.staticforms.xyz/submit" method="post">
			<Label class="label" for="name">Name</Label>
			<Input class="input" id="name" name="name" type="text" placeholder="Ihr Name" />
			<Label class="label" for="email">E-Mail</Label>
			<Input class="input" id="email" name="email" type="email" placeholder="Ihre E-Mail" />
			<Label class="label" for="message">Nachricht</Label>
			<textarea class="textarea" id="message" name="message" placeholder="Ihre Nachricht"></textarea>
			<button class="contactButton" type="submit">Absenden</button>
			<input type="text" name="honeypot" style="display:none">
			<input type="hidden" name="accessKey" value="598031a5-631e-458d-8613-4b86d81aaa8e">
			<input type="hidden" name="subject" value="Kontaktformular kunst-heuwes-ahlers.de" />
			<input type="hidden" name="redirectTo" value="https://kunst-heuwes-ahlers.de/kontakt">
			<input type="hidden" name="replyTo" value="@">
		</form>
	</div>
</div>

<style>
	.contactButton {
		outline: black;
		color: black;
		border: solid 1px #000;
		border-radius: 4px;
		width: 100%;
	}
	.input {
		max-width: 300px;
		padding: 10px;
		margin-bottom: 1em;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
	}
	.label {
		padding: 4px;
	}
	textarea {
		width: 100%;
		height: 150px;
		padding: 10px;
		margin-bottom: 1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
		box-sizing: border-box;
	}
	@media screen and (max-width: 768px) {
		.main {
			display: flex;
			flex-flow: column wrap;
			justify-content: center;
			align-items: center;
			min-height: 80vh;
		}
		.contactForm {
			padding-right: 0;
			width: 100%;
		}
		.contactDescription {
			width: 100%;
			padding-left: 0;
		}
	}
	@media screen and (min-width: 769px) {
		.main {
			display: flex;
			flex-flow: row wrap;
			justify-content: center;
			align-items: center;
			min-height: 80vh;
		}
		.contactForm {
			padding-right: 20%;
			width: 50%;
			text-align: left;
		}
		.contactDescription {
			width: 50%;
			padding-left: 20%;
            padding-right: 5%;
			text-align: left;
		}
	}

	h1 {
		font-size: 2rem;
		font-weight: 700;
		margin-bottom: 1rem;
	}
	h4 {
		padding-top: 20px;
		font-size: 1.5rem;
		font-weight: 700;
		margin-bottom: 1rem;
	}
	p {
		margin-bottom: 1rem;

	}
</style>
