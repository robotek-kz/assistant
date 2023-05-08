<template>
    <div>
        <div class="development-window">
            <p class="development-text">Страница в разработке</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UnderDevelopment'
}

</script>

<style lang="sass">

.development-window
  display: flex
  justify-content: center
  align-items: center
  height: 100vh


.development-text
  font-size: 350%
  color: #212121
  text-align: center

</style>