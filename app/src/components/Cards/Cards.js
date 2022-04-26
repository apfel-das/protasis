import React from "react";
import { Grid, Typography } from "@material-ui/core";

import CardComponent from "../Card/Card";
import styles from './Cards.module.css';


class Cards extends React.Component
{
    
    
    render() {
        
        /**
         * Decompose params.
         */
        const {users, movies, ratings, handler, selectedCard} = this.props;

        return(
            <div className={styles.container}>
                    <Grid container 
                        spacing={2} 
                        justifyContent="center"
                        wrap="nowrap"
                        sx={{
                            overflow: 'auto',
                            }}
                    >
                    <CardComponent
                        className={styles.left}
                        cardTitle="Users"
                        value={users}
                        cardSubtitle="Number of users in records."
                        clickHandler={handler}
                        selectedCard={selectedCard}
                    />
                    <CardComponent
                        className={styles.mid}
                        cardTitle="Movies"
                        value={movies}
                        cardSubtitle="Number of movies in records."
                        clickHandler={handler}
                        selectedCard={selectedCard}
                    />
                    <CardComponent
                        className={styles.right}
                        cardTitle="Ratings"
                        value={ratings}
                        cardSubtitle="Number movie-ratings from users."
                        clickHandler={handler}
                        selectedCard={selectedCard}
                    />
                    <CardComponent
                        className={styles.rightmost}
                        cardTitle="Recommendations"
                        values={null}
                        cardSubtitle="Get movie recommendations based on KNN or SVD algorithm (for a specific user)."
                        clickHandler={handler}
                        selectedCard={selectedCard}
                    />
                </Grid>
            </div>
        );
    }
}

export default Cards;