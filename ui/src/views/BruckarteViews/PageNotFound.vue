<template>
    <div class="contents">
      <section>
        <h1 class="opa">...OPA!
        </h1>

        <p class="p404">
          Izgleda da tražena stranica ne postoji!         <br>
          Obrati se svom savjetniku za pomoć.
        </p>
        

      </section>

    </div>
</template>
  
<script>

export default {
  name: 'PageNotFound',
}
</script>
  
<style>

.opa {
  font-size: 128px !important;
  font-weight: 700 !important;
  text-align: center;
  margin-bottom: 5rem !important;
  margin-top: 5rem !important;

}

.p404 {
  font-size: 24px !important;
  font-weight: 400;
  text-align: center;
  margin-top: 5rem !important;
}
</style>