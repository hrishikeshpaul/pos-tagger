import { FC, useState } from 'react';

import { Box } from '@chakra-ui/react';

import { Navbar } from 'components/navbar';
import { Tagger } from 'components/tagger/Tagger';

import './App.scss';
import { Loader } from 'components/loader/Loader';
import { useEffect } from 'react';
import { getHealth } from 'util/Service';

export const App: FC = () => {
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<boolean>(true);

    useEffect(() => {
        (async () => {
            try {
                setLoading(true);
                await getHealth();
                setLoading(false);
            } catch (err) {
                setLoading(false);
            }
        })();
    }, []);

    return (
        <Box className="App">
            {loading ? (
                <Loader />
            ) : (
                <>
                    <Navbar />
                    <Box pt="83px" h="100%" w="100%">
                        <Tagger />
                    </Box>
                </>
            )}
        </Box>
    );
};
