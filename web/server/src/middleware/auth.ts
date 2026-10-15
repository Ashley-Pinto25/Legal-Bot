import type { NextFunction, Request, Response } from "express";
import jwt from "jsonwebtoken";
export type AuthRequest = Request & { user?: { id:string; role:string } };
export function signToken(user:{id:string;role:string}) { return jwt.sign(user, process.env.JWT_SECRET || "development-only-change-me", { expiresIn:"7d" }); }
export function requireAuth(req:AuthRequest,res:Response,next:NextFunction) { try { const token=req.header("authorization")?.replace("Bearer ",""); if(!token) throw Error(); req.user=jwt.verify(token, process.env.JWT_SECRET || "development-only-change-me") as {id:string;role:string}; next(); } catch { res.status(401).json({error:"Authentication required"}); } }
export function requireAdmin(req:AuthRequest,res:Response,next:NextFunction) { if(req.user?.role!=="admin") return res.status(403).json({error:"Administrator access required"}); next(); }
