// let BASE_API_URL = 'http://localhost:5000';

import jwtService from './jwt.service';


class ApiService {
  constructor(onError) {
    this.onError = onError;
    this.base_url = 'http://localhost:5000/api';
  }

  async request(options) {
    let response = await ApiService.requestInternal(options);
    if (response.status === 401 && options.url !== '/tokens') {
      const refreshResponse = await this.put('/tokens', {
        access_token: jwtService.getToken(),
      });
      if (refreshResponse.ok) {
        const body = await refreshResponse.body;
        jwtService.setToken(body.access_token);
        response = ApiService.requestInternal(options);
      }
    }
    if (response.status >= 500 && this.onError) {
      console.log('error', response);
      // this.onError(response);
    }
    return response;
  }

  static async requestInternal(options) {
    let query = new URLSearchParams(options.query || {}).toString();

    if (query !== '') {
      query = `?${query}`;
    }

    let response;
    try {
      console.log('wtf', options.body);
      response = await fetch(`http://localhost:5000/api${options.url}${query}`, {
        method: options.method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('id_token')}`,
          ...options.headers,
        },
        credentials: options.url === '/tokens' ? 'include' : 'omit',
        body: options.body ? JSON.stringify(options.body) : null,
      });
      console.log('resp', response);
    } catch (error) {
      response = {
        ok: false,
        status: 500,
        json: async () => ({
          code: 500,
          message: 'The server is unresponsive',
          description: error.toString(),
        }),
      };
    }
    return {
      ok: response.ok,
      status: response.status,
      body: response.status !== 204 ? response.json() : null,
    };
  }

  async upload(endpoint, body, episode) {
    const response = await fetch(`http://localhost:5000/api${endpoint}`, {
      body,
      config: { headers: {
              'Content-Type': 'multipart/form-data'
          }},
      method: "POST"
      });
    return {
      ok: response.ok,
      status: response.status,
      body: response.status !== 204 ? response.json() : null,
    };
  
    
    // return fetch(`${this.base_url}/${endpoint}`, {
    //   formData,
    //   config: { headers: {
    //           'Content-Type': 'multipart/form-data'
    //       }},
    //   method: "POST"
    //   })
    // return this.request("/", formData, {
    //   headers: {
    //     "Content-Type": "multipart/form-data"
    //   },
    //   onUploadProgress
    // });
  }

  async get(url, query, options) {
    return this.request({
      method: 'GET', url, query, ...options,
    });
  }

  async post(url, body, options) {
    return this.request({
      method: 'POST', url, body, ...options,
    });
  }

  async put(url, body, options) {
    // console.log('put body', body);
    return this.request({
      method: 'PUT', url, body, ...options,
    });
  }

  async delete(url, options) {
    return this.request({
      method: 'DELETE', url, ...options,
    });
  }

  async login(nickname, password) {
    const response = await this.post('/tokens', null, {
      headers: {
        Authorization: `Basic ${btoa(`${nickname}:${password}`)}`,
      },
    });
    console.log('Resp:', response);
    console.log('Response:', response.ok);
    console.log('Status:', response.status);
    if (!response.ok) {
      return response.status === 401 ? 'fail' : 'error';
    }
    // localStorage.setItem('accessToken', response.body.access_token);
    return response;
  }


  async logout() {
    await this.delete('/tokens');
    localStorage.removeItem('id_token');
  }

  static isAutheticated() {
    return localStorage.getItem('id_token') !== null;
  }
}

export default ApiService;
