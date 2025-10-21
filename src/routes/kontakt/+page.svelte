<script>
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
      <!-- <label class="label" for="name">Name</label> -->
      <input class="input" id="name" name="name" type="text" placeholder="Ihr Name" />
      
      <!-- <label class="label" for="email">E-Mail</label> -->
      <input class="input" id="email" name="email" type="email" placeholder="Ihre E-Mail" />
      
      <!-- <label class="label" for="message">Nachricht</label> -->
      <textarea class="textarea" id="message" name="message" placeholder="Ihre Nachricht"></textarea>
      
      <button class="btn" type="submit">Absenden</button>
      
      <input type="text" name="honeypot" style="display:none">
      <input type="hidden" name="accessKey" value="598031a5-631e-458d-8613-4b86d81aaa8e">
      <input type="hidden" name="subject" value="Kontaktformular kunst-heuwes-ahlers.de" />
      <input type="hidden" name="redirectTo" value="https://kunst-heuwes-ahlers.de/kontakt">
      <input type="hidden" name="replyTo" value="@">
    </form>
  </div>
</div>

<style>
.input:focus {
  outline: none;
  border-color: black;
}

textarea:focus {
  outline: none;
  border-color: black;
}

@media screen and (max-width: 768px) {
  .main {
    display: flex;
    flex-flow: column wrap;
    justify-content: center;
    align-items: flex-start;
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