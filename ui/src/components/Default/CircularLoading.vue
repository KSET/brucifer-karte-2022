<template>
    <v-dialog v-if="dialog" width="90px" >
      <v-card  height="90px" style="overflow:hidden">
        <v-progress-circular size="90px" indeterminate color="black"></v-progress-circular>
      </v-card>

    </v-dialog>
</template>

<script>
// to use this component, import it in the other component, and pass an argument dialog into it, dialog = true starts loading animation and false stops it
export default {
    name: 'CircularLoading',
    props: [
        'dialog',
    ]
}
</script>
