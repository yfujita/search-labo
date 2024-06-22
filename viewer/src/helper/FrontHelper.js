/**
 * FrontHelper.js
 * 
 * This module provides helper functions for front.
 */
export default function () {

  /**
   * Get Url Parameters
   * @returns {Object<string, string[]>}
   */
  const getUrlParameters = () => {
    let hash = '';
    let url = location.href;
    if (url.indexOf('#') != -1) {
      const array = url.split('#');
      url = array[0];
      hash = array[1];
    }

    // Parse url parameters.
    const params = (url => {
      const params = {};
      if (url.indexOf('?') != -1) {
        const array = url.split('?');
        const paramArray = array[1].split('&');
        paramArray.forEach((val, index, ar) => {
          const tpl = val.split('=');
          const key = decodeURIComponent(tpl[0]);
          let value = '';
          if (tpl.length > 1) {
            value = decodeURIComponent(tpl[1].replace(new RegExp("\\+", 'g'), '%20'));
          }

          if (params[key] === undefined) {
            params[key] = [value];
          } else {
            params[key].push(value);
          }
        });
      }
      return params;
    })(url);

    params['fess_url_hash'] = hash;
    return params;
  };

  return {
    getUrlParameters,
  };
}