/*  Copyright (C) 2006, 2007 William McCune

    This file is part of the LADR Deduction Library.

    The LADR Deduction Library is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License,
    version 2.

    The LADR Deduction Library is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with the LADR Deduction Library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
*/

#ifndef TP_XPROOFS_H
#define TP_XPROOFS_H

#include "clauses.h"
#include "clause_misc.h"
#include "paramod.h"
#include "subsume.h"

/* INTRODUCTION
*/

/* Public definitions */

/* End of public definitions */

/* Public function prototypes from xproofs.c */

void check_parents_and_uplinks_in_proof(Plist proof);

Topform proof_id_to_clause(Plist proof, int id);

int greatest_id_in_proof(Plist proof);

Plist expand_proof(Plist proof, I3list *pmap);

void renumber_proof(Plist proof, int start);

Plist copy_and_renumber_proof(Plist proof, int start);

Plist proof_to_xproof(Plist proof);

#endif  /* conditional compilation of whole file */
