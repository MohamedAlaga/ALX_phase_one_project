import { NAV_LINKS } from "@/constants"
import Image from "next/image"
import Link from "next/link"
import Button from "./button"

import React from 'react';

const Navbar = () => {
  return (
    <nav className="flexBetween max-container padding-container relative z-30 py-5">
      <Link href="/">
        <Image src="/public\image.png" alt="logo" width={74} height={29} />
      </Link>
    </nav>
  );
};

export default Navbar;