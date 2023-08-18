from telegrambot.cli import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.mode == "message":
        send_message(args)
    elif args.mode == "photo":
        send_photo(args)
    elif args.mode == "updates":
        get_updates(args)
    else:
        raise ValueError(f"Invalid mode {args.mode}")


if __name__ == "__main__":
    main()
