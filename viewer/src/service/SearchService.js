import axios from 'axios';
import Mustache from 'mustache';

import searchTemplateBasic from '@/assets/search-template/basic.mustache';
import searchTemplateKnn from '@/assets/search-template/knn.mustache';


/**
 * SearchService.js
 * 
 * This module provides search functions.
 */
export default class {
  constructor(esUrl){
    this.esUrl = esUrl.endsWith('/') ? esUrl.substring(0, esUrl.length - 1): esUrl;
    this.mlApiUrl = 'http://localhost:18081';
  }
  
  /**
   * Get fess version.
   * @returns fessVersion
   */
  getFessVersion() {
    const url = this.esUrl + '/json';
    return new Promise((resolve, reject) =>  {
      try {
        axios.get(
          url
        ).then((res) => {
          const version = res.data.response.version;
          resolve(version);
        }).catch((e) => {
          console.log('ERROR!!');
          reject(e);
        });
      } catch (e) {
        console.log('ERROR!!!');
        reject(e);
      }
    });
  }

  /**
   * Search
   * @param {Object} searchCond 
   * @param {Object} state Update by search result.
   * @returns Promise<SearchResponse>
   */
  async search(searchCond) {
    let url;
    let query;
    if (searchCond.searchType === 'basic') {
      url = `${this.esUrl}/search-basic/_search`;
      const searchParams = this._buildBasicParams(searchCond);
      query = this._renderQuery(searchTemplateBasic, searchParams);
    } else if (searchCond.searchType === 'knn') {
      url = `${this.esUrl}/search-knn/_search`;
      const searchParams = await this._buildKnnParams(searchCond);
      query = this._renderQuery(searchTemplateKnn, searchParams);
    } else {
      throw new Error('Invalid search type.' + searchCond.type);
    }

    console.log('Search cond...', searchCond);
    console.log('Search start...', query);

    const response = await axios.post(
      url,
      query,
      {
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );
    console.log('Search success!', response.data);
    return response.data;
  }

  /**
   * Build params for basic search.
   */
  _buildBasicParams(searchCond) {
    const searchParams = {
      keywords: searchCond.q.split(/[\u0020\u3000]+/),
      sort: searchCond.sort,
      from: (searchCond.page - 1) * searchCond.pageSize,
      size: searchCond.pageSize,
    };
    return searchParams;
  }

  /**
   * Build params for knn search.
   */
  async _buildKnnParams(searchCond) {
    const url = this.mlApiUrl + '/api/vectorize/bert';
    const response = await axios.post(
      url,
      {
        text: 'タイトルが「' + searchCond.q + '」の記事'
      },
      {
        headers: {
          'Content-Type': 'application/json',
        }
      }
    );

    const searchParams = {
      keywords: searchCond.q.split(/[\u0020\u3000]+/),
      sort: searchCond.sort,
      from: (searchCond.page - 1) * searchCond.pageSize,
      size: searchCond.pageSize,
      query_vector: response.data.vector,
    };
    return searchParams;
  }

  /**
   * Render query
   */
  _renderQuery(template, searchParams) {
    const rendered = Mustache.render(template, searchParams);
    return rendered.replace(/,(?=\s*[}\]])/g, '');
  }
}