# monte-carlo-parley
a monte carlo simulation for poker hands written in RUST

# psuedocode
```RUST
use rand::seq::SliceRandom;
use rand::thread_rng;
use std::fmt;

// Card representation
#[derive(Debug, Clone, Copy, PartialEq)]
enum Suit {
    Clubs,
    Diamonds,
    Hearts,
    Spades,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Rank {
    Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten,
    Jack, Queen, King, Ace,
}

#[derive(Debug, Clone, Copy, PartialEq)]
struct Card {
    rank: Rank,
    suit: Suit,
}

impl fmt::Display for Card {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let rank_str = match self.rank {
            Rank::Two => "2", Rank::Three => "3", Rank::Four => "4",
            Rank::Five => "5", Rank::Six => "6", Rank::Seven => "7",
            Rank::Eight => "8", Rank::Nine => "9", Rank::Ten => "10",
            Rank::Jack => "J", Rank::Queen => "Q", Rank::King => "K",
            Rank::Ace => "A",
        };
        let suit_str = match self.suit {
            Suit::Clubs => "♣", Suit::Diamonds => "♦",
            Suit::Hearts => "♥", Suit::Spades => "♠",
        };
        write!(f, "{}{}", rank_str, suit_str)
    }
}

// Deck representation
struct Deck {
    cards: Vec<Card>,
}

impl Deck {
    fn new() -> Deck {
        let mut cards = Vec::new();
        let suits = [Suit::Clubs, Suit::Diamonds, Suit::Hearts, Suit::Spades];
        let ranks = [
            Rank::Two, Rank::Three, Rank::Four, Rank::Five, Rank::Six,
            Rank::Seven, Rank::Eight, Rank::Nine, Rank::Ten, Rank::Jack,
            Rank::Queen, Rank::King, Rank::Ace,
        ];
        for &suit in suits.iter() {
            for &rank in ranks.iter() {
                cards.push(Card { rank, suit });
            }
        }
        Deck { cards }
    }

    fn remove(&mut self, card: Card) {
        if let Some(index) = self.cards.iter().position(|&c| c == card) {
            self.cards.remove(index);
        }
    }

    fn shuffle(&mut self) {
        let mut rng = thread_rng();
        self.cards.shuffle(&mut rng);
    }

    fn deal(&mut self) -> Option<Card> {
        self.cards.pop()
    }
}

// Simplified hand evaluation (returns a score)
fn evaluate_hand(cards: &[Card]) -> u32 {
    // For simplicity, just count distinct ranks (basic pair detection)
    // In a real implementation, check for all poker hands
    let mut counts = [0; 13];
    for card in cards {
        let rank_idx = match card.rank {
            Rank::Two => 0, Rank::Three => 1, Rank::Four => 2, Rank::Five => 3,
            Rank::Six => 4, Rank::Seven => 5, Rank::Eight => 6, Rank::Nine => 7,
            Rank::Ten => 8, Rank::Jack => 9, Rank::Queen => 10, Rank::King => 11,
            Rank::Ace => 12,
        };
        counts[rank_idx] += 1;
    }
    let max_count = counts.iter().max().unwrap_or(&0);
    if *max_count >= 2 { *max_count } else { 1 } // Pair = 2, High card = 1
}

fn monte_carlo_simulation(
    my_hole: [Card; 2],
    opp_hole: [Card; 2],
    flop: [Card; 3],
    num_simulations: usize,
) -> f64 {
    let mut deck = Deck::new();
    let known_cards = vec![my_hole[0], my_hole[1], opp_hole[0], opp_hole[1], flop[0], flop[1], flop[2]];
    for card in &known_cards {
        deck.remove(*card);
    }

    let mut wins = 0;
    let mut ties = 0;

    for _ in 0..num_simulations {
        let mut sim_deck = deck.clone();
        sim_deck.shuffle();

        let turn = sim_deck.deal().unwrap();
        let river = sim_deck.deal().unwrap();

        let my_hand: Vec<Card> = my_hole.iter().chain(&flop).chain(&[turn, river]).copied().collect();
        let opp_hand: Vec<Card> = opp_hole.iter().chain(&flop).chain(&[turn, river]).copied().collect();

        let my_score = evaluate_hand(&my_hand);
        let opp_score = evaluate_hand(&opp_hand);

        if my_score > opp_score {
            wins += 1;
        } else if my_score == opp_score {
            ties += 1;
        }
    }

    let total = num_simulations as f64;
    (wins as f64 + ties as f64 * 0.5) / total // Win probability (split ties)
}

fn main() {
    let my_hole = [
        Card { rank: Rank::Ace, suit: Suit::Spades },
        Card { rank: Rank::King, suit: Suit::Spades },
    ];
    let opp_hole = [
        Card { rank: Rank::Queen, suit: Suit::Hearts },
        Card { rank: Rank::Jack, suit: Suit::Hearts },
    ];
    let flop = [
        Card { rank: Rank::Ten, suit: Suit::Spades },
        Card { rank: Rank::Four, suit: Suit::Diamonds },
        Card { rank: Rank::Two, suit: Suit::Clubs },
    ];

    let odds = monte_carlo_simulation(my_hole, opp_hole, flop, 10_000);
    println!("Your win probability: {:.2}%", odds * 100.0);
}
```

