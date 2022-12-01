import logo from './logo.svg';
import './App.css';
import { Golf } from './golf';
import { Container, Grid, Box } from '@mui/material';
import {ReactComponent as Background} from './background.svg'

function App() {
  return (
    <div className="App"
    // style={{ backgroundImage: `url(${background})`, backgroundSize: "cover"}}
    >
        <Container maxWidth="sm">
          <Grid
              container
              spacing={0}
              direction="column"
              alignItems="center"
              justifyContent="center"
              style={{ minHeight: '100vh' }}
          >
            <Box sx={{ 
              bgcolor: 'background.paper', 
              boxShadow: 1,
              borderRadius: 2,
              p: 2,
            }}>
              <Golf></Golf>
            </Box>
          </Grid> 
        </Container>
    </div>
  );
}

export default App;
