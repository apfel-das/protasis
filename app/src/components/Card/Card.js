import React from 'react';
import { Card, CardContent, Typography, Grid } from '@material-ui/core';
import CountUp from 'react-countup';
import cx from 'classnames';
import DoneIcon from '@mui/icons-material/Done';
import styles from './Card.module.css';



class CardComponent extends React.Component{
  


  render(){
    /**
     * Deref. params.
     */
    const {className, cardTitle, value, cardSubtitle, clickHandler, selectedCard} = this.props;
    
 

    return(
      <Grid 
        item xs={12} md={3} component={Card} className={cx(styles.card, className)}
        onClick={() => {clickHandler(cardTitle)}} 
       
      >
        <CardContent>
          
          <Typography color="textSecondary" gutterBottom>
            {cardTitle}
          </Typography>
          <Typography variant="h5" component="h2">
            {value ? <CountUp start={0} end={value} duration={2.75} separator="." /> : null}
          </Typography>
          <Typography variant="body2" component="p">
            {cardSubtitle}
          </Typography>
          {(selectedCard === cardTitle)  ? <DoneIcon style={{color: "green"}}/> : null }
        </CardContent>
      </Grid>
    );
  }
}
 

export default CardComponent;