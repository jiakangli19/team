<template>
    <div>
      <h1>Twitter</h1>
      <p>This is the twitter page content.</p>
      <button @click="getData">testdata</button>
      <ul>
        <li v-for="(item, index) in data" :key="index">{{ item }}</li> 
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    name: 'TwitterAll',
    props:{
      msg: String
    },
    data() {
      return{
        data: [],
      };
    },
    methods: {
      async getData() {
        try {
          const response = await axios.get('http://172.26.133.42:8000/getTest');
          console.log(response.data);
          this.data = response.data;
       
        } catch (error) {
          console.log(error);
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .twitterall {
    text-align: center;
    margin-top: 20px;
  }
  </style>
  
  