import { createApp } from 'vue/dist/vue.esm-bundler';
import SearchForm from '@/components/basic/search-form/SearchForm';
import SearchResult from '@/components/basic/search-result/SearchResult';

const init = () => {
  console.log("Initialize fess-site-search...");
  const app = createApp({
    components: {
      'search-form': SearchForm,
      'search-result': SearchResult,
    }
  });
  app.mount('#search-labo');
};

window.addEventListener('DOMContentLoaded', init);
