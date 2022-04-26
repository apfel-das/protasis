import React from 'react';
import styles from './App.module.css';
import client from './components/AxiosConf';
import Cards from './components/Cards/Cards';
import Table from './components/Table/Table';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import logo from './images/logo.png';
import { ButtonGroup } from '@mui/material';




class App extends React.Component{

  
  constructor(props)
  {
    super(props);

    /**
     * Encapsulate everything as Component's state.
     */
    this.state = {
      movies: null,
      moviesCount: 0,
      users: null,
      usersCount: 0,
      ratings: null,
      ratingsCount: 0,
      selectedCard: "",
      errorMessage: null,
      tableData: null,
      tableKeys: null,
      selectedUser: null,    
      knnRecommendations: null,
      svdRecommendations: null,
      selectedAlgo: "",
      recommendationsActive: false,
      promptMessage: 'Pick a category to display.'
    }

    
    this.handleDataChange = this.handleDataChange.bind(this);
    this.handleUserSelection = this.handleUserSelection.bind(this);
    
  }



  /**
   * Handle the selection of a specific user from MUI DataGrid.
   * @param {*} userRow The selected row.
   */
  async handleUserSelection(userRow){

    
    
    if(this.state.selectedCard === "Recommendations" && this.state.recommendationsActive === false){
      
      /**
       * Block on data receival.
       */
      await this.retrieveRecommendations(userRow.row.user_id);
      
      this.setState({
        selectedUser: userRow,
        recommendationsActive: true,
        tableKeys: Object.keys(this.state.knnRecommendations[0]),
        tableData: (this.state.selectedAlgo === "KNN") ? this.state.knnRecommendations : this.state.svdRecommendations
        
      });
     
    }
    

  }

  /***
   * Handles the data source change on common array.
   * Note: mutates the state of parent component.
   */
  handleDataChange(cardTitle){
    

    if (cardTitle === 'Ratings'){
      this.setState(
        {
          selectedUser: null,
          selectedCard: cardTitle,
          tableData: this.state.ratings,
          tableKeys: Object.keys(this.state.ratings[0]),
          promptMessage: 'Pick a category to display.',
          recommendationsActive: false
        }
      );
    }
    else if (cardTitle === 'Movies'){
      this.setState(
        {
          selectedUser: null,
          selectedCard: cardTitle,
          tableData: this.state.movies,
          tableKeys: Object.keys(this.state.movies[0]),
          promptMessage: 'Pick a category to display.',
          recommendationsActive: false
        }
      );
    }
    else if(cardTitle === 'Users'){
      this.setState(
        {
          selectedCard: cardTitle,
          tableData: this.state.users,
          tableKeys: Object.keys(this.state.users[0]),
          promptMessage: 'Pick a category to display.', 
          recommendationsActive: false
        }
      );
    }
    else if(cardTitle === 'Recommendations'){
      this.setState(
        {
          selectedCard: cardTitle,
          tableData: this.state.users,
          tableKeys: Object.keys(this.state.users[0]),
          promptMessage: 'Pick any user to get recommendations',
          recommendationsActive: false,
          selectedAlgo: "KNN"

        }
      );
    }

  }


  /**
   * Retrieve movie recommendations (both svd, knn algo) for the userId specified.
   * @param {*} userId  The respective user_id.
   */
  async retrieveRecommendations(userId){
    
    try {
      /**
       * KNN endpoint.
       */
      await client.get('/recommendations/knn/'+userId)
      .then(response => {

          let recommendedMovies = [];
          response.data.forEach(movieId => {
            recommendedMovies.push(this.state.movies[movieId-1]);
          });
          this.setState({knnRecommendations: recommendedMovies});
          })
      .catch(error => {
          console.log(error);
          this.setState({errorMessage: error});
      });

      /**
       * SVD endpoint.
      */
      await client.get('/recommendations/svd/'+userId)
      .then(response => {
          let recommendedMovies = [];
          response.data.forEach(movieId => {
            recommendedMovies.push(this.state.movies[movieId-1]);
          });
          this.setState({svdRecommendations: recommendedMovies});
          })
      .catch(error => {
          console.log(error);
          this.setState({errorMessage: error});
      });
    }
    catch (error) {
      console.log(error);
      this.setState({errorMessage: error});
    }
  }
    /**
   * Retrieve user data from API's endpoint.
   */
  async retrieveUsers(){
    await client.get('/users' )
    .then(response => {
        this.setState({
          users: response.data,
          usersCount: response.data.length
        });
        })
    .catch(error => {
        console.log(error);
        this.setState({errorMessage: error.message});
    });
  }
  
  /**
   * Retrieve movies data from API's endpoint.
   */
  async retrieveMovies(){
      await client.get('/movies' )
      .then(response => {
          this.setState({
            movies: response.data,
            moviesCount: response.data.length
          });
        })
      .catch(error => {
          console.log(error);
          this.setState({errorMessage: error.message});
      });
  }

  /**
   * Retrieve ratings data from API's endpoint.
   */
  async retrieveRatings(){
    await client.get('/ratings' )
      .then(response => {
        this.setState({
          ratings: response.data,
          ratingsCount: response.data.length
        });
      })
      .catch(error => {
          console.log(error);
          this.setState({errorMessage: error.message});
      });
  }

  /**
   * On mount, block on data retrieval.
   */
  async componentDidMount(){
    await this.retrieveRatings();   
    await this.retrieveUsers();
    await this.retrieveMovies(); 
    
  }

  render(){
  
  
    return(
      
      <div className={styles.container}>
        <img className={styles.image} src={logo} alt="logo" />

        {
        
        (!this.state.errorMessage) ?

        <>
          <Cards
            users={this.state.usersCount}
            ratings={this.state.ratingsCount}
            movies={this.state.moviesCount}
            handler={this.handleDataChange}
            selectedCard={this.state.selectedCard}
          />
          <Alert severity='info' variant='filled' sx={{marginBottom: '3%'}}>
            {this.state.promptMessage}
          </Alert>
        
          {(this.state.recommendationsActive === true) ? 
          <ButtonGroup variant="primary" size = "large" aria-label="outlined large button group" 
          sx={
            {
              backgroundImage: 'linear-gradient(to right, #ff9966, #993030)',
              borderRadius: '10px',
              borderStyle: 'solid',
              display: 'inline-flex',
              opacity: '1',
              transition: 'opacity 700ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
              width:'230px',
              marginBottom: '1.5%'
            }
          }
          >
            <Button 
              onClick={() => {this.setState({selectedAlgo: "KNN", tableData: this.state.knnRecommendations})}}
              sx={
                {
                  color: '#f5f5f5',
                  width: '50%'
                }
              }
            >
              KNN
            </Button>
            <Button 
              onClick={() => {this.setState({selectedAlgo: "SVD", tableData: this.state.svdRecommendations})}}
              sx={
                  {
                    color: '#f5f5f5',
                    width: '50%'
                  }
                }
            >
              SVD
            </Button>
          </ButtonGroup>
          : null
          }
          
          <Table
            rows={this.state.tableData}
            columns={this.state.tableKeys}
            userSelectionHandler={this.handleUserSelection}
          />
        </>
        : 
        <Alert severity='error' variant='filled' sx={{marginBottom: '5%'}}>
            {this.state.errorMessage + ". Please try again in a while.."}
        </Alert>
        }

      </div>
    );
  }

}

export default App;
