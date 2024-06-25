<script>
import { defineComponent, reactive} from "vue";

/**
 * Component for search result items.
 */
export default defineComponent({
  props: {
    enableThumbnail: {
      type: Boolean,
      default: false,
    },
    searchHit: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },

  setup(props, context) {
    console.log('item');

    const _existThumbnail = () => {
      return false;
    };

    const _title = () => {
      return props.searchHit._source.title;
    };

    const _description = () => {
      if (props.searchHit.highlight === undefined) {
        return props.searchHit._source.content.substring(0, 40) + '...';
      } else if (props.searchHit.highlight.content !== undefined) {
        return props.searchHit.highlight.content;
      } else if (props.searchHit.highlight['content.tk'] !== undefined) {
        return props.searchHit.highlight['content.tk'];
      } else {
        return props.searchHit._source.content.substring(0, 40) + '...';
      }
    };

    const _url = () => {
      return props.searchHit._source.url;
    };

    const _score = () => {
      return props.searchHit._score;
    };

    // reactive data
    const state = reactive({
      existThumbnail: _existThumbnail(),
      title: _title(),
      description: _description(),
      url: _url(),
      score: _score(),
    });

    // method definitions

    /**
     * Format date string.
     */
    const formatDate = (date) => {
      if (date == null) {
        return '';
      }
      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      const hours = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();
      return year + '-' + month.toString().padStart(2, '0') 
        + '-' + day.toString().padStart(2, '0') + ' ' 
        + hours.toString().padStart(2, '0') + ':'
        + minutes.toString().padStart(2, '0') + ':'
        + seconds.toString().padStart(2, '0');
    };
    
    // Format content length string.
    const formatContentLength = (contentLength) => {
      const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
      let l = 0, n = parseInt(contentLength, 10) || 0;

      while(n >= 1024 && ++l) {
        n = n/1024;
      }

      //include a decimal point and a tenths-place digit if presenting 
      //less than ten of KB or greater units
      return(n.toFixed(n < 10 && l > 0 ? 1 : 0) + ' ' + units[l]);
    };

    // Set the presence of a thumbnail.
    const hasThumbnail = (element) => {
      state.existThumbnail = true;
    };

    // Set the absence of a thumbnail.
    const noThumbnail = (element) => {
      state.existThumbnail = false;
    };

    return {
      state,
      formatDate,
      formatContentLength,
      hasThumbnail,
      noThumbnail,
    };
  }
});
</script>

<template>
  <div>
    <h3 class="title text-truncate">
      <a
        class="link"
        :href="state.url"
        target="_blank"
        v-html="state.title"
      />
    </h3>
    <div class="body">
      <div v-if="enableThumbnail" v-show="state.existThumbnail" class="mr-3">
        <a
          class="link d-none d-sm-flex"
          :href="state.url"
          target="_blank"
        >
          <img
            src=""
            alt="thumbnail"
            class="thumbnail"
          >
        </a>
      </div>
      <div class="description" v-html="state.description" />
    </div>
    <div class="site text-truncate">
      <cite>{{ state.url }}</cite>
    </div>
    <div class="info">
      <small>
        <span v-if="state.score > 0">
          - score {{ state.score }}&nbsp;
        </span>
      </small>
    </div>
  </div>
</template>