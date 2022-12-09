import { ChangeEvent, FC, useState } from 'react';

import { Box, Button, Center, Container, Divider, Flex, Input, Text } from '@chakra-ui/react';

import { getTags, Tag } from 'util/Service';
import { Abbreviations } from 'util/Contants';

import './Tagger.scss';

enum State {
    Input,
    Result,
}

export const Tagger: FC = () => {
    const [state, setState] = useState<State>(State.Input);
    const [loading, setLoading] = useState<boolean>(false);
    const [form, setForm] = useState<{ sentence: string }>({ sentence: '' });
    const [response, setResponse] = useState<Tag[]>([]);

    const onChange = (e: ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, sentence: e.target.value });
    };

    const onSubmit = async (e: ChangeEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        const results = await getTags(form.sentence);

        setResponse(results);
        setLoading(false);
        setState(State.Result);
    };

    const onReset = () => {
        setState(State.Input);
        setResponse([]);
        setForm({ sentence: '' });
    };

    const Form: FC = () => {
        return (
            <form style={{ width: '100%' }} onSubmit={onSubmit}>
                <Flex flexDir="column" gap="6" w="100%" alignItems="center">
                    <Input
                        fontSize={{ base: '36px', md: '48px' }}
                        fontWeight="800"
                        w="100%"
                        variant="flushed"
                        borderBottomWidth="2px"
                        borderColor="black"
                        placeholder="Type a sentence..."
                        py="8"
                        type="text"
                        autoFocus
                        name="sentence"
                        required
                        onChange={onChange}
                        value={form.sentence}
                        _placeholder={{ opacity: 0.2 }}
                        _focusVisible={{ boxShadow: 'none', borderColor: 'pink.400' }}
                        readOnly={loading}
                    />
                    <Box w={{ base: '100%', md: '25%' }}>
                        <Button
                            w="100%"
                            size="lg"
                            type="submit"
                            disabled={!form.sentence.length || loading}
                            isLoading={loading}
                            loadingText="Tagging sentence..."
                        >
                            Submit
                        </Button>
                    </Box>
                </Flex>
            </form>
        );
    };

    const Result: FC = () => {
        return (
            <Flex w="100%" alignItems="center" flexDir="column" className="results">
                <Flex gap="4" w="100%" justifyContent="center" flexWrap="wrap">
                    {response.map((item, i) => {
                        return (
                            <Box position="relative" className="results-box" key={i}>
                                <Box>
                                    <Text textAlign="center" fontSize={{ base: '36px', md: '48px' }} fontWeight="800">
                                        {item.word}
                                    </Text>
                                    <Divider borderWidth="2px" />
                                    <Text fontWeight="500" textAlign="center">
                                        {Abbreviations[item.tag]}
                                    </Text>
                                </Box>
                                <Text
                                    className="results-prob"
                                    color="gray.500"
                                    fontSize="sm"
                                    fontWeight="600"
                                    textAlign="center"
                                >
                                    {item.prob.toFixed(2)}%
                                </Text>
                            </Box>
                        );
                    })}
                </Flex>
                <Box mt="16" w={{ base: '100%', md: '25%' }}>
                    <Button w="100%" size="lg" colorScheme="gray" onClick={onReset}>
                        Try again
                    </Button>
                </Box>
            </Flex>
        );
    };

    return (
        <Container className="post-tagger" h="100%" maxW="5xl">
            <Center h="90%">{state === State.Input ? <Form /> : <Result />}</Center>
        </Container>
    );
};
