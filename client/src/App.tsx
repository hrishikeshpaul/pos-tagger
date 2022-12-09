import { FC } from 'react';

import { Box } from '@chakra-ui/react';

import { Navbar } from 'components/navbar';
import { Tagger } from 'components/tagger/Tagger';

import './App.scss';

export const App: FC = () => {
    return (
        <Box className="App">
            <Navbar />
            <Box pt="83px" h="100%" w="100%">
                <Tagger />
            </Box>
        </Box>
    );
};
