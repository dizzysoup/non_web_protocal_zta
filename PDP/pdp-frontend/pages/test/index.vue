<template>
  <div>
    <c-button left-icon="check" mb="3" variant-color="blue" @click="open" variant="outline">Open Modal</c-button>
    <c-modal
      :is-open="isOpen"
      :on-close="close"
    >
      <c-modal-content ref="content">
        <c-modal-header>Modal Title</c-modal-header>
        <c-modal-close-button />
        <c-modal-body>
          <Lorem add="2s" />
        </c-modal-body>
        <c-modal-footer>
          <c-button variant-color="blue" mr="3">
            Save
          </c-button>
          <c-button @click="close">Cancel</c-button>
        </c-modal-footer>
      </c-modal-content>
      <c-modal-overlay />
    </c-modal>
  </div>
</template>

<script>
export default {
  data () {
    return {
      isOpen: false
    }
  },
  methods: {
    open() {
      this.isOpen = true
    },
    close() {
      this.isOpen = false
    }
  }
}
</script>