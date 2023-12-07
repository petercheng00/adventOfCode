use aoc2023_rust::read_input;

fn main() {
    let input_str = read_input();
    part1(&input_str);
    part2(&input_str);
}

fn part1(input: &str) {
    let mut hands_and_bids = load_hands_and_bids(input, false);

    hands_and_bids.sort();

    let mut total = 0;
    for (i, (_hand, bid)) in hands_and_bids.iter().enumerate() {
        total += (i + 1) as u32 * bid;
    }
    println!("Part 1 total: {}", total);
}

fn part2(input: &str) {
    let mut hands_and_bids = load_hands_and_bids(input, true);

    hands_and_bids.sort();

    let mut total = 0;
    for (i, (_hand, bid)) in hands_and_bids.iter().enumerate() {
        total += (i + 1) as u32 * bid;
    }
    println!("Part 2 total: {}", total);
}

fn char_to_value(c: char, jokers: bool) -> u8 {
    c.to_digit(10).unwrap_or_else(|| match c {
        'T' => 10,
        'J' => {
            if jokers {
                0
            } else {
                11
            }
        }
        'Q' => 12,
        'K' => 13,
        'A' => 14,
        _ => panic!("Invalid card value: {}", c),
    }) as u8
}

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
enum HandType {
    HighCard,
    OnePair,
    TwoPairs,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

#[derive(Debug, Eq, PartialEq)]
struct Hand {
    cards: Vec<u8>,
    jokers: bool,
}

impl Hand {
    fn new(hand_str: &str, jokers: bool) -> Self {
        Hand {
            cards: hand_str.chars().map(|c| char_to_value(c, jokers)).collect(),
            jokers,
        }
    }

    fn get_hand_type(&self) -> HandType {
        let mut card_to_count = [0; 15];
        let mut joker_count = 0;
        for &card in &self.cards {
            if card == 0 {
                joker_count += 1;
            } else {
                card_to_count[card as usize] += 1;
            }
        }
        let mut count_counts = [0; 6];
        for count in card_to_count {
            count_counts[count as usize] += 1;
        }

        let pre_joker_type = if count_counts[5] == 1 {
            HandType::FiveOfAKind
        } else if count_counts[4] == 1 {
            HandType::FourOfAKind
        } else if count_counts[3] == 1 && count_counts[2] == 1 {
            HandType::FullHouse
        } else if count_counts[3] == 1 {
            HandType::ThreeOfAKind
        } else if count_counts[2] == 2 {
            HandType::TwoPairs
        } else if count_counts[2] == 1 {
            HandType::OnePair
        } else if count_counts[1] >= 1 {
            HandType::HighCard
        } else {
            assert!(self.jokers && joker_count == 5);
            return HandType::FiveOfAKind;
        };
        if !self.jokers || joker_count == 0 {
            return pre_joker_type;
        }

        // It's always better to make all jokers the same value.
        let max_count = card_to_count.iter().max().unwrap();
        let new_max_count = max_count + joker_count;

        match new_max_count {
            5 => HandType::FiveOfAKind,
            4 => HandType::FourOfAKind,
            3 => {
                if pre_joker_type == HandType::TwoPairs {
                    HandType::FullHouse
                } else {
                    HandType::ThreeOfAKind
                }
            }
            2 => HandType::OnePair,
            _ => panic!("Invalid new max count: {}", new_max_count),
        }
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let self_type = self.get_hand_type();
        let other_type = other.get_hand_type();
        if self_type != other_type {
            return self_type.cmp(&other_type);
        }
        self.cards.cmp(&other.cards)
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

fn load_hands_and_bids(input: &str, jokers: bool) -> Vec<(Hand, u32)> {
    let mut hands_and_bids = Vec::new();
    for line in input.lines() {
        let (hand_str, bid_str) = line.split_once(' ').unwrap();
        hands_and_bids.push((Hand::new(hand_str, jokers), bid_str.parse::<u32>().unwrap()));
    }
    hands_and_bids
}
